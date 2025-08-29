// File: server/api/chat-stream.post.ts
import { GoogleGenerativeAI, HarmCategory, HarmBlockThreshold } from "@google/generative-ai";

interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

interface SimulationResults {
  aco?: {
    bestMakespan?: string | number;
    executionTime?: string | number;
    loadBalanceIndex?: string | number;
    computationTime?: string | number;
    finalAssignment?: any[];
  };
  pso?: {
    bestMakespan?: string | number;
    executionTime?: string | number;
    loadBalanceIndex?: string | number;
    computationTime?: string | number;
    finalAssignment?: any[];
  };
}

interface RequestBody {
  userMessage: string;
  simulationResults: SimulationResults;
  swarmType: string; // "ACO", "PSO", or "both"
  chatHistory?: ChatMessage[];
  language?: string;
}

// SSE helper to write events to the stream
async function writeSSE(event: any, type: string, data: any) {
  const sseData = `data: ${JSON.stringify({ type, data })}\n\n`;
  if (event.node?.res?.write) {
    event.node.res.write(sseData);
  }
}

export default defineEventHandler(async (event) => {
  // Set SSE headers
  setHeader(event, "Content-Type", "text/event-stream");
  setHeader(event, "Cache-Control", "no-cache");
  setHeader(event, "Connection", "keep-alive");

  try {
    const body: RequestBody = await readBody(event);
    const {
      userMessage = "Explain the results",
      simulationResults,
      swarmType,
      chatHistory = [],
      language = "English",
    } = body;

    const apiKey = process.env.GEMINI_API_KEY;
    if (!apiKey) {
      throw new Error("Gemini API key not configured");
    }

    const genAI = new GoogleGenerativeAI(apiKey);

    // 1. Build the system message with simulation data
    const systemMessage = buildSystemMessage(simulationResults, swarmType, language);

    // 2. Initialize the model with the system message
    const model = genAI.getGenerativeModel({
      model: "gemini-1.5-flash",
      systemInstruction: systemMessage,
       safetySettings: [ // Add safety settings to avoid blocking
        {
          category: HarmCategory.HARM_CATEGORY_HARASSMENT,
          threshold: HarmBlockThreshold.BLOCK_NONE,
        },
        {
          category: HarmCategory.HARM_CATEGORY_HATE_SPEECH,
          threshold: HarmBlockThreshold.BLOCK_NONE,
        },
        {
          category: HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
          threshold: HarmBlockThreshold.BLOCK_NONE,
        },
        {
          category: HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
          threshold: HarmBlockThreshold.BLOCK_NONE,
        },
      ],
    });

    // 3. Start a chat session with previous history
    const chat = model.startChat({
      history: chatHistory
        .slice(-6) // Use last 6 messages for context
        .map(msg => ({
          role: msg.role === 'assistant' ? 'model' : 'user',
          parts: [{ text: msg.content }]
        })),
    });

    await writeSSE(event, "start", "Starting AI response...");

    // 4. Send only the new user message to the chat stream
    const result = await chat.sendMessageStream(userMessage);

    for await (const chunk of result.stream) {
      const chunkText = chunk.text();
      if (chunkText) {
        await writeSSE(event, "chunk", chunkText);
      }
    }

    await writeSSE(event, "done", "Response complete");

  } catch (err: any) {
    console.error("Chat Stream API Error:", err);
    await writeSSE(
      event,
      "error",
      err instanceof Error ? err.message : "An internal server error occurred."
    );
  } finally {
    // Ensure the response stream is ended.
    if (event.node?.res?.end) {
      event.node.res.end();
    }
  }
});


// system prompt builder
function buildSystemMessage(sim: SimulationResults, swarmType: string, language: string): string {
  const prompts: any = {
    English: {
      system:
        "You are Swarm Lab AI Assistant, specialized in analyzing and explaining simulation results. The front-end ALWAYS sends complete simulation data automatically. NEVER ask users to provide raw data, metrics, or upload files - you already have everything needed. When users say vague things like 'explain results', 'jelaskan hasilnya', 'compare', or 'which is best', you must analyze the latest simulationResults directly. Output must be structured in Markdown with clear sections, tables, and bullet points. Be concise, analytical, and structured. Provide insights and comparisons, not just descriptions. Treat simulationResults as the single source of truth. Never say 'I didn't receive data' - if the object exists, assume it is valid.",
      results: "📊 Current Simulation Results",
      aco: "🐜 ACO (Ant Colony Optimization)",
      pso: "🐦 PSO (Particle Swarm Optimization)",
      analysis: "📈 Performance Analysis",
      insights: "💡 Key Insights",
      comparison: "🔍 Algorithm Comparison",
    },
    Indonesian: {
      system:
        "Anda adalah Asisten AI Swarm Lab, khusus dalam menganalisis dan menjelaskan hasil simulasi. Front-end SELALU mengirim data simulasi lengkap secara otomatis. TIDAK PERNAH meminta pengguna untuk memberikan data mentah, metrik, atau mengunggah file - Anda sudah memiliki semua yang dibutuhkan. Ketika pengguna mengatakan hal-hal umum seperti 'jelaskan hasilnya', 'bandingkan', atau 'yang terbaik', Anda harus langsung menganalisis simulationResults terbaru. Keluaran harus terstruktur dalam Markdown dengan bagian yang jelas, tabel, dan poin-poin. Ringkas, analitis, dan terstruktur. Berikan wawasan dan perbandingan, bukan hanya deskripsi. Perlakukan simulationResults sebagai sumber kebenaran tunggal. Jangan pernah mengatakan 'saya tidak menerima data' - jika objek ada, anggap valid.",
      results: "📊 Hasil Simulasi Saat Ini",
      aco: "🐜 ACO (Ant Colony Optimization)",
      pso: "🐦 PSO (Particle Swarm Optimization)",
      analysis: "📈 Analisis Kinerja",
      insights: "💡 Wawasan Utama",
      comparison: "🔍 Perbandingan Algoritma",
    },
    Chinese: {
      system:
        "您是Swarm Lab AI助手，专门分析和解释模拟结果。前端始终自动发送完整的模拟数据。绝不要求用户提供原始数据、指标或上传文件 - 您已经拥有所需的一切。当用户说模糊的话如'解释结果'、'比较'或'哪个最好'时，您必须直接分析最新的simulationResults。输出必须用Markdown结构化，包含清晰部分、表格和要点。简洁、分析性强、结构化。提供见解和比较，而非仅描述。将simulationResults视为唯一真实来源。绝不说'我没收到数据' - 如果对象存在，假设其有效。",
      results: "📊 当前模拟结果",
      aco: "🐜 ACO（蚁群优化）",
      pso: "🐦 PSO（粒子群优化）",
      analysis: "📈 性能分析",
      insights: "💡 关键见解",
      comparison: "🔍 算法比较",
    },
  };

  const p = prompts[language] || prompts["English"];
  let context = `${p.system}\n\nRespond in ${language}. Use proper Markdown formatting with tables, bullet points, and clear sections. Always analyze based on the provided simulationResults object. Never ask for missing data; assume it's complete.`;

  // Build analysis based on swarmType parameter
  context += `\n\n## ${p.results}\n`;
  
  const hasAco = swarmType.includes('ACO') && sim.aco;
  const hasPso = swarmType.includes('PSO') && sim.pso;

  if (hasAco) {
    context += `\n### ${p.aco}\n`;
    context += `| Metric | Value |\n|--------|--------|`;
    context += `\n| **Best Makespan** | ${Number(sim.aco?.bestMakespan || 0).toFixed(2)} |`;
    context += `\n| **Execution Time** | ${Number(sim.aco?.executionTime || 0).toFixed(2)} |`;
    context += `\n| **Load Balance Index** | ${Number(sim.aco?.loadBalanceIndex || 0).toFixed(4)} |`;
    context += `\n| **Agents** | ${sim.aco?.finalAssignment?.length ?? 0} |`;
  }
  
  if (hasPso) {
    context += `\n\n### ${p.pso}\n`;
    context += `| Metric | Value |\n|--------|--------|`;
    context += `\n| **Best Makespan** | ${Number(sim.pso?.bestMakespan || 0).toFixed(2)} |`;
    context += `\n| **Execution Time** | ${Number(sim.pso?.executionTime || 0).toFixed(2)} |`;
    context += `\n| **Load Balance Index** | ${Number(sim.pso?.loadBalanceIndex || 0).toFixed(4)} |`;
    context += `\n| **Agents** | ${sim.pso?.finalAssignment?.length ?? 0} |`;
  }
  
  if (hasAco && hasPso) {
    context += `\n\n### ${p.comparison}\n`;
    const winner = getBetterAlgorithm(sim);
    context += `- **Winner**: ${winner}\n`;
  }

  return context;
}

// Helper function to determine better algorithm
function getBetterAlgorithm(sim: SimulationResults): string {
  const acoMakespan = parseFloat(String(sim.aco?.bestMakespan ?? Infinity));
  const psoMakespan = parseFloat(String(sim.pso?.bestMakespan ?? Infinity));
  
  if (acoMakespan < psoMakespan) return "ACO (better makespan)";
  if (psoMakespan < acoMakespan) return "PSO (better makespan)";
  return "Tie (equal performance)";
}
