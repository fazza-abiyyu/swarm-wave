// File: server/api/chat-stream.post.ts
import { GoogleGenAI } from "@google/genai";

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

export default defineEventHandler(async (event) => {
  // SSE headers
  setHeader(event, "Content-Type", "text/event-stream");
  setHeader(event, "Cache-Control", "no-cache");
  setHeader(event, "Connection", "keep-alive");

  try {
    const body: RequestBody = await readBody(event);
    const {
      userMessage = "",
      simulationResults,
      swarmType,
      chatHistory = [],
      language = "English",
    } = body;

    const sim = simulationResults;

    const apiKey = process.env.GEMINI_API_KEY;
    if (!apiKey) {
      await writeSSE(event, "error", "Gemini API key not configured");
      return;
    }

    // init Gemini client
    const ai = new GoogleGenAI({ apiKey });

    // system message
    const systemMessage = buildSystemMessage(sim, swarmType, language);

    // build chat contents
    const chatParts: string[] = [];
    if (chatHistory && chatHistory.length > 0) {
      chatHistory.slice(-6).forEach((msg) => {
        chatParts.push(
          `${msg.role === "user" ? "User" : "Assistant"}: ${msg.content}`
        );
      });
    }
    chatParts.push(`User: ${userMessage}`);

    const finalPrompt = `${systemMessage}\n\n${chatParts.join("\n")}`;

    // kirim start SSE
    await writeSSE(event, "start", "Starting response...");

    // streaming response dari Gemini SDK baru
    const stream = await ai.models.generateContentStream({
      model: "gemini-2.5-flash",
      contents: finalPrompt,
    });

    // iterate langsung, tanpa `.stream`
    for await (const chunk of stream) {
      const text = chunk.text;
      if (text) {
        await writeSSE(event, "chunk", text);
      }
    }

    // selesai
    await writeSSE(event, "done", "Response complete");
  } catch (err: any) {
    console.error("Chat Stream API Error:", err);
    await writeSSE(
      event,
      "error",
      err instanceof Error ? err.message : "Internal server error"
    );
  }
});

// system prompt builder
function buildSystemMessage(sim: SimulationResults, swarmType: string, language: string): string {
  const prompts: any = {
    English: {
      system:
        "You are Swarm Lab AI Assistant, specialized in analyzing and explaining simulation results. The front-end ALWAYS sends complete simulation data (`simulationResults`) automatically. NEVER ask users to provide raw data, metrics, or upload files - you already have everything needed. When users say vague things like 'explain results', 'jelaskan hasilnya', 'compare', or 'which is best', you must analyze the latest simulationResults directly. Output must be structured in Markdown with clear sections, tables, and bullet points. Be concise, analytical, and structured. Provide insights and comparisons, not just descriptions. Treat simulationResults as the single source of truth. Never say 'I didn't receive data' - if the object exists, assume it is valid.",
      results: "📊 Current Simulation Results",
      aco: "🐜 ACO (Ant Colony Optimization)",
      pso: "🐦 PSO (Particle Swarm Optimization)",
      analysis: "📈 Performance Analysis",
      insights: "💡 Key Insights",
      comparison: "🔍 Algorithm Comparison",
    },
    Indonesian: {
      system:
        "Anda adalah Asisten AI Swarm Lab, khusus dalam menganalisis dan menjelaskan hasil simulasi. Front-end SELALU mengirim data simulasi lengkap (`simulationResults`) secara otomatis. TIDAK PERNAH meminta pengguna untuk memberikan data mentah, metrik, atau mengunggah file - Anda sudah memiliki semua yang dibutuhkan. Ketika pengguna mengatakan hal-hal umum seperti 'jelaskan hasilnya', 'bandingkan', atau 'yang terbaik', Anda harus langsung menganalisis simulationResults terbaru. Keluaran harus terstruktur dalam Markdown dengan bagian yang jelas, tabel, dan poin-poin. Ringkas, analitis, dan terstruktur. Berikan wawasan dan perbandingan, bukan hanya deskripsi. Perlakukan simulationResults sebagai sumber kebenaran tunggal. Jangan pernah mengatakan 'saya tidak menerima data' - jika objek ada, anggap valid.",
      results: "📊 Hasil Simulasi Saat Ini",
      aco: "🐜 ACO (Ant Colony Optimization)",
      pso: "🐦 PSO (Particle Swarm Optimization)",
      analysis: "📈 Analisis Kinerja",
      insights: "💡 Wawasan Utama",
      comparison: "🔍 Perbandingan Algoritma",
    },
    Chinese: {
      system:
        "您是Swarm Lab AI助手，专门分析和解释模拟结果。前端始终自动发送完整的模拟数据（`simulationResults`）。绝不要求用户提供原始数据、指标或上传文件 - 您已经拥有所需的一切。当用户说模糊的话如'解释结果'、'比较'或'哪个最好'时，您必须直接分析最新的simulationResults。输出必须用Markdown结构化，包含清晰部分、表格和要点。简洁、分析性强、结构化。提供见解和比较，而非仅描述。将simulationResults视为唯一真实来源。绝不说'我没收到数据' - 如果对象存在，假设其有效。",
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
  
  if (swarmType === "both") {
    // Show both ACO and PSO results with comparison
    context += `\n### ${p.aco}\n`;
    context += `| Metric | Value |\n|--------|--------|`;
    context += `\n| **Best Makespan** | ${sim.aco?.bestMakespan ?? "N/A"} |`;
    context += `\n| **Execution Time** | ${sim.aco?.executionTime ?? "N/A"} |`;
    context += `\n| **Load Balance Index** | ${sim.aco?.loadBalanceIndex ?? "N/A"} |`;
    context += `\n| **Computation Time** | ${sim.aco?.computationTime ?? "N/A"} |`;
    context += `\n| **Agents** | ${sim.aco?.finalAssignment?.length ?? 0} |`;
    
    context += `\n\n### ${p.pso}\n`;
    context += `| Metric | Value |\n|--------|--------|`;
    context += `\n| **Best Makespan** | ${sim.pso?.bestMakespan ?? "N/A"} |`;
    context += `\n| **Execution Time** | ${sim.pso?.executionTime ?? "N/A"} |`;
    context += `\n| **Load Balance Index** | ${sim.pso?.loadBalanceIndex ?? "N/A"} |`;
    context += `\n| **Computation Time** | ${sim.pso?.computationTime ?? "N/A"} |`;
    context += `\n| **Agents** | ${sim.pso?.finalAssignment?.length ?? 0} |`;
    
    // Add comparison section
    context += `\n\n### ${p.comparison}\n`;
    context += `**ACO vs PSO Analysis:**\n`;
    context += `- **Makespan**: ${sim.aco?.bestMakespan ?? "N/A"} vs ${sim.pso?.bestMakespan ?? "N/A"} seconds\n`;
    context += `- **Winner**: ${getBetterAlgorithm(sim)}\n`;
    context += `- **Efficiency**: Lower makespan = better performance\n`;
    context += `- **Balance**: Lower load balance index = better task distribution\n`;
    
  } else if (swarmType === "ACO") {
    // Show only ACO results
    context += `\n### ${p.aco}\n`;
    context += `| Metric | Value |\n|--------|--------|`;
    context += `\n| **Best Makespan** | ${sim.aco?.bestMakespan ?? "N/A"} |`;
    context += `\n| **Execution Time** | ${sim.aco?.executionTime ?? "N/A"} |`;
    context += `\n| **Load Balance Index** | ${sim.aco?.loadBalanceIndex ?? "N/A"} |`;
    context += `\n| **Computation Time** | ${sim.aco?.computationTime ?? "N/A"} |`;
    context += `\n| **Agents** | ${sim.aco?.finalAssignment?.length ?? 0} |`;
    
  } else if (swarmType === "PSO") {
    // Show only PSO results
    context += `\n### ${p.pso}\n`;
    context += `| Metric | Value |\n|--------|--------|`;
    context += `\n| **Best Makespan** | ${sim.pso?.bestMakespan ?? "N/A"} |`;
    context += `\n| **Execution Time** | ${sim.pso?.executionTime ?? "N/A"} |`;
    context += `\n| **Load Balance Index** | ${sim.pso?.loadBalanceIndex ?? "N/A"} |`;
    context += `\n| **Computation Time** | ${sim.pso?.computationTime ?? "N/A"} |`;
    context += `\n| **Agents** | ${sim.pso?.finalAssignment?.length ?? 0} |`;
  }

  // Add insights section
  context += `\n\n## ${p.insights}\n`;
  context += getAnalysisInsights(sim, swarmType);

  return context;
}

// Helper function to determine better algorithm
function getBetterAlgorithm(sim: SimulationResults): string {
  const acoMakespan = parseFloat(String(sim.aco?.bestMakespan || "0"));
  const psoMakespan = parseFloat(String(sim.pso?.bestMakespan || "0"));
  
  if (isNaN(acoMakespan) || isNaN(psoMakespan)) return "ACO vs PSO (data comparison pending)";
  if (acoMakespan === 0 && psoMakespan === 0) return "N/A";
  if (acoMakespan === 0) return "PSO";
  if (psoMakespan === 0) return "ACO";
  
  if (acoMakespan < psoMakespan) return "ACO (better makespan)";
  if (psoMakespan < acoMakespan) return "PSO (better makespan)";
  return "Tie (equal performance)";
}

// Helper function to generate analysis insights
function getAnalysisInsights(sim: SimulationResults, swarmType: string): string {
  let insights = "";
  
  if (swarmType === "both") {
    const acoMakespan = parseFloat(String(sim.aco?.bestMakespan || "0"));
    const psoMakespan = parseFloat(String(sim.pso?.bestMakespan || "0"));
    const acoBalance = parseFloat(String(sim.aco?.loadBalanceIndex || "0"));
    const psoBalance = parseFloat(String(sim.pso?.loadBalanceIndex || "0"));
    
    insights += `**Algorithm Comparison:**\n`;
    insights += `- **Best Makespan**: ${getBetterAlgorithm(sim)} performs better\n`;
    insights += `- **Load Balance**: ${acoBalance < psoBalance ? "ACO" : "PSO"} has better task distribution\n`;
    insights += `- **Efficiency**: Consider both makespan and load balance\n`;
    insights += `- **Recommendation**: Use ${getBetterAlgorithm(sim)} for optimal performance\n`;
    
  } else if (swarmType === "ACO") {
    const acoMakespan = parseFloat(String(sim.aco?.bestMakespan || "0"));
    const acoBalance = parseFloat(String(sim.aco?.loadBalanceIndex || "0"));
    
    insights += `**ACO Analysis:**\n`;
    insights += `- **Performance**: Makespan of ${acoMakespan || "N/A"} seconds\n`;
    insights += `- **Balance**: Load balance index of ${acoBalance || "N/A"}\n`;
    insights += `- **Optimization**: Tune parameters for better convergence\n`;
    insights += `- **Scalability**: Evaluate agent utilization efficiency\n`;
    
  } else if (swarmType === "PSO") {
    const psoMakespan = parseFloat(String(sim.pso?.bestMakespan || "0"));
    const psoBalance = parseFloat(String(sim.pso?.loadBalanceIndex || "0"));
    
    insights += `**PSO Analysis:**\n`;
    insights += `- **Performance**: Makespan of ${psoMakespan || "N/A"} seconds\n`;
    insights += `- **Balance**: Load balance index of ${psoBalance || "N/A"}\n`;
    insights += `- **Convergence**: Evaluate swarm optimization efficiency\n`;
    insights += `- **Parameters**: Consider swarm size and iteration count\n`;
  }
  
  return insights;
}

// SSE helper
async function writeSSE(event: any, type: string, data: string) {
  const sseData = `data: ${JSON.stringify({ type, data })}\n\n`;
  if (event.node?.res?.write) {
    event.node.res.write(sseData);
  } else if (event.response?.write) {
    event.response.write(sseData);
  }
}
