import { ChatOpenAI } from "@langchain/openai";
import { AIMessage, HumanMessage, SystemMessage } from "@langchain/core/messages";

const config = useRuntimeConfig();

// --- INTERFACES (No changes needed) ---
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
    convergenceData?: number[];
    ganttChartHtml?: string;
    totalAgents?: number;
    totalTasks?: number;
    parameters?: {
      alpha?: number;
      beta?: number;
      evaporation_rate?: number;
      pheromone_deposit?: number;
      n_ants?: number;
    };
  };
  pso?: {
    bestMakespan?: string | number;
    executionTime?: string | number;
    loadBalanceIndex?: string | number;
    computationTime?: string | number;
    finalAssignment?: any[];
    convergenceData?: number[];
    ganttChartHtml?: string;
    totalAgents?: number;
    totalTasks?: number;
    parameters?: {
      n_particles?: number;
      w?: number;
      c1?: number;
      c2?: number;
    };
  };
  dataSpecification?: {
    totalRows?: number;
    totalColumns?: number;
    columns?: string[];
    sampleData?: any[];
    dataTypes?: Record<string, string>;
    dataLimitations?: {
      originalRows?: number;
      filteredRows?: number;
      showAllData?: boolean;
      dataLimit?: number;
    };
  };
  algorithmParameters?: {
    common?: {
      num_default_agents?: number;
      n_iterations?: number;
      task_id_col?: string;
      agent_id_col?: string;
    };
    aco?: any;
    pso?: any;
  };
}

interface RequestBody {
  userMessage: string;
  simulationResults: SimulationResults;
  swarmType: string; // "ACO", "PSO", or "both"
  chatHistory?: ChatMessage[];
  language?: string;
}

// --- SSE HELPER (No changes needed) ---
async function writeSSE(event: any, type: string, data: any) {
  const sseData = `data: ${JSON.stringify({ type, data })}\n\n`;
  if (event.node?.res?.write) {
    event.node.res.write(sseData);
  }
}

// --- EVENT HANDLER (Modified for LangChain OpenAI) ---
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

    // Use OpenAI API Key from runtime config
    const apiKey = config.EXNEST_API_KEY || process.env.EXNEST_API_KEY;
    if (!apiKey) {
      throw new Error("Exnest API key not configured");
    }

    // 1. Build the system message with simulation data (same logic)
    const systemPrompt = buildSystemMessage(simulationResults, swarmType, language);

    // 2. Initialize the LangChain OpenAI model for streaming
    const model = new ChatOpenAI({
      apiKey: apiKey,
      modelName: config.MODELS || "gpt-4.1-mini", // Default to gpt-4.1-mini if not specified
      configuration: { baseURL: config.EXNEST_BASE_URL || "https://api.exnest.app/v1" },
      temperature: 0.5,
      streaming: true,
    });
    
    // 3. Construct the message history for LangChain
    const messages = [
        new SystemMessage(systemPrompt),
        // Map previous chat history to LangChain message format
        ...chatHistory.slice(-6).map(msg => {
            return msg.role === 'assistant' 
                ? new AIMessage(msg.content) 
                : new HumanMessage(msg.content);
        }),
        // Add the new user message
        new HumanMessage(userMessage),
    ];


    await writeSSE(event, "start", "Starting AI response...");

    // 4. Get the streaming response from the model
    const stream = await model.stream(messages);

    // 5. Write each chunk from the stream to the SSE response
    for await (const chunk of stream) {
      const chunkText = chunk.content;
      if (typeof chunkText === 'string' && chunkText.length > 0) {
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


// --- SYSTEM PROMPT BUILDER (No changes needed) ---
function buildSystemMessage(sim: SimulationResults, swarmType: string, language: string): string {
  const prompts: any = {
    English: {
      system:
        "You are Swarm Wave AI Assistant, specialized in analyzing and explaining simulation results. The front-end ALWAYS sends complete simulation data automatically including parameters and data specifications. NEVER ask users to provide raw data, metrics, parameters, or upload files - you already have everything needed. When users say vague things like 'explain results', 'jelaskan hasilnya', 'compare', or 'which is best', you must analyze the latest simulationResults directly. Output must be structured in Markdown with clear sections, tables, and bullet points. Be concise, analytical, and structured. Provide insights and comparisons, not just descriptions. Treat simulationResults as the single source of truth. Never say 'I didn't receive data' - if the object exists, assume it is valid.",
      results: "📊 Current Simulation Results",
      dataSpec: "📁 Data Specification",
      parameters: "⚙️ Algorithm Parameters",
      aco: "🐜 ACO (Ant Colony Optimization)",
      pso: "🐦 PSO (Particle Swarm Optimization)",
      analysis: "📈 Performance Analysis",
      insights: "💡 Key Insights",
      comparison: "🔍 Algorithm Comparison",
    },
    Indonesian: {
      system:
        "Anda adalah Asisten AI Swarm Wave, khusus dalam menganalisis dan menjelaskan hasil simulasi. Front-end SELALU mengirim data simulasi lengkap secara otomatis termasuk parameter dan spesifikasi data. TIDAK PERNAH meminta pengguna untuk memberikan data mentah, metrik, parameter, atau mengunggah file - Anda sudah memiliki semua yang dibutuhkan. Ketika pengguna mengatakan hal-hal umum seperti 'jelaskan hasilnya', 'bandingkan', atau 'yang terbaik', Anda harus langsung menganalisis simulationResults terbaru. Keluaran harus terstruktur dalam Markdown dengan bagian yang jelas, tabel, dan poin-poin. Ringkas, analitis, dan terstruktur. Berikan wawasan dan perbandingan, bukan hanya deskripsi. Perlakukan simulationResults sebagai sumber kebenaran tunggal. Jangan pernah mengatakan 'saya tidak menerima data' - jika objek ada, anggap valid.",
      results: "📊 Hasil Simulasi Saat Ini",
      dataSpec: "📁 Spesifikasi Data",
      parameters: "⚙️ Parameter Algoritma",
      aco: "🐜 ACO (Ant Colony Optimization)",
      pso: "🐦 PSO (Particle Swarm Optimization)",
      analysis: "📈 Analisis Kinerja",
      insights: "💡 Wawasan Utama",
      comparison: "🔍 Perbandingan Algoritma",
    },
    Chinese: {
      system:
        "您是Swarm Wave AI助手，专门分析和解释模拟结果。前端始终自动发送完整的模拟数据，包括参数和数据规格。绝不要求用户提供原始数据、指标、参数或上传文件 - 您已经拥有所需的一切。当用户说模糊的话如'解释结果'、'比较'或'哪个最好'时，您必须直接分析最新的simulationResults。输出必须用Markdown结构化，包含清晰部分、表格和要点。简洁、分析性强、结构化。提供见解和比较，而非仅描述。将simulationResults视为唯一真实来源。绝不说'我没收到数据' - 如果对象存在，假设其有效。",
      results: "📊 当前模拟结果",
      dataSpec: "📁 数据规格",
      parameters: "⚙️ 算法参数",
      aco: "🐜 ACO（蚁群优化）",
      pso: "🐦 PSO（粒子群优化）",
      analysis: "📈 性能分析",
      insights: "💡 关键见解",
      comparison: "🔍 算法比较",
    },
  };

  const p = prompts[language] || prompts["English"];
  let context = `${p.system}\n\nRespond in ${language}. Use proper Markdown formatting with tables, bullet points, and clear sections. Always analyze based on the provided simulationResults object. Never ask for missing data; assume it's complete.`;

  // Add data specification section
  if (sim.dataSpecification) {
    context += `\n\n## ${p.dataSpec}\n`;
    const ds = sim.dataSpecification;
    const filteredRows = ds.dataLimitations?.filteredRows || ds.totalRows || 0;
    const originalRows = ds.dataLimitations?.originalRows || ds.totalRows || 0;
    
    context += `| Property | Value |\n|----------|-------|`;
    context += `\n| **Dataset Rows** | ${filteredRows}${originalRows !== filteredRows ? ` (filtered from ${originalRows})` : ''} |`;
    context += `\n| **Dataset Columns** | ${ds.totalColumns || 0} |`;
    context += `\n| **Column Headers** | ${ds.columns?.join(', ') || 'N/A'} |`;
    
    if (ds.dataTypes) {
      context += `\n| **Data Types** | ${Object.entries(ds.dataTypes).map(([col, type]) => `${col}: ${type}`).join(', ')} |`;
    }
    
    if (ds.sampleData && ds.sampleData.length > 0) {
      context += `\n\n**Sample Data (first 3 rows):**\n`;
      context += `| ${ds.columns?.join(' | ') || ''} |\n|${ds.columns?.map(() => '---').join('|') || ''}|`;
      ds.sampleData.slice(0, 3).forEach(row => {
        const values = ds.columns?.map(col => row[col] || 'N/A').join(' | ') || '';
        context += `\n| ${values} |`;
      });
    }
  }

  // Add algorithm parameters section
  if (sim.algorithmParameters) {
    context += `\n\n## ${p.parameters}\n`;
    const ap = sim.algorithmParameters;
    
    if (ap.common) {
      context += `\n### Common Parameters\n`;
      context += `| Parameter | Value |\n|-----------|-------|`;
      context += `\n| **Agents** | ${ap.common.num_default_agents || 'N/A'} |`;
      context += `\n| **Iterations** | ${ap.common.n_iterations || 'N/A'} |`;
      context += `\n| **Task ID Column** | ${ap.common.task_id_col || 'N/A'} |`;
      context += `\n| **Agent ID Column** | ${ap.common.agent_id_col || 'N/A'} |`;
    }
    
    if (ap.aco && swarmType.includes('ACO')) {
      context += `\n\n### ACO Parameters\n`;
      context += `| Parameter | Value |\n|-----------|-------|`;
      context += `\n| **Alpha (Pheromone)** | ${ap.aco.alpha || 'N/A'} |`;
      context += `\n| **Beta (Heuristic)** | ${ap.aco.beta || 'N/A'} |`;
      context += `\n| **Evaporation Rate** | ${ap.aco.evaporation_rate || 'N/A'} |`;
      context += `\n| **Pheromone Deposit** | ${ap.aco.pheromone_deposit || 'N/A'} |`;
      context += `\n| **Number of Ants** | ${ap.aco.n_ants || 'N/A'} |`;
    }
    
    if (ap.pso && swarmType.includes('PSO')) {
      context += `\n\n### PSO Parameters\n`;
      context += `| Parameter | Value |\n|-----------|-------|`;
      context += `\n| **Particles** | ${ap.pso.n_particles || 'N/A'} |`;
      context += `\n| **Inertia Weight (w)** | ${ap.pso.w || 'N/A'} |`;
      context += `\n| **Cognitive Factor (c1)** | ${ap.pso.c1 || 'N/A'} |`;
      context += `\n| **Social Factor (c2)** | ${ap.pso.c2 || 'N/A'} |`;
    }
  }

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
    context += `\n| **Agents** | ${sim.aco?.totalAgents ?? sim.algorithmParameters?.common?.num_default_agents ?? 0} |`;
    context += `\n| **Tasks Processed** | ${sim.aco?.totalTasks ?? sim.dataSpecification?.dataLimitations?.filteredRows ?? sim.dataSpecification?.totalRows ?? 0} |`;
    context += `\n| **Final Assignments** | ${sim.aco?.finalAssignment?.length ?? 0} agent groups |`;
  }
  
  if (hasPso) {
    context += `\n\n### ${p.pso}\n`;
    context += `| Metric | Value |\n|--------|--------|`;
    context += `\n| **Best Makespan** | ${Number(sim.pso?.bestMakespan || 0).toFixed(2)} |`;
    context += `\n| **Execution Time** | ${Number(sim.pso?.executionTime || 0).toFixed(2)} |`;
    context += `\n| **Load Balance Index** | ${Number(sim.pso?.loadBalanceIndex || 0).toFixed(4)} |`;
    context += `\n| **Agents** | ${sim.pso?.totalAgents ?? sim.algorithmParameters?.common?.num_default_agents ?? 0} |`;
    context += `\n| **Tasks Processed** | ${sim.pso?.totalTasks ?? sim.dataSpecification?.dataLimitations?.filteredRows ?? sim.dataSpecification?.totalRows ?? 0} |`;
    context += `\n| **Final Assignments** | ${sim.pso?.finalAssignment?.length ?? 0} agent groups |`;
  }
  
  if (hasAco && hasPso) {
    context += `\n\n### ${p.comparison}\n`;
    const winner = getBetterAlgorithm(sim);
    context += `- **Winner**: ${winner}\n`;
    
    const acoParams = sim.algorithmParameters?.aco;
    const psoParams = sim.algorithmParameters?.pso;
    
    if (acoParams) {
      context += `- **ACO Configuration**: α=${acoParams.alpha}, β=${acoParams.beta}, ρ=${acoParams.evaporation_rate}, ${acoParams.n_ants} ants\n`;
    }
    if (psoParams) {
      context += `- **PSO Configuration**: w=${psoParams.w}, c1=${psoParams.c1}, c2=${psoParams.c2}, ${psoParams.n_particles} particles\n`;
    }
  }

  return context;
}

// --- HELPER FUNCTION (No changes needed) ---
function getBetterAlgorithm(sim: SimulationResults): string {
  const acoMakespan = parseFloat(String(sim.aco?.bestMakespan ?? Infinity));
  const psoMakespan = parseFloat(String(sim.pso?.bestMakespan ?? Infinity));
  
  if (acoMakespan < psoMakespan) return "ACO (better makespan)";
  if (psoMakespan < acoMakespan) return "PSO (better makespan)";
  return "Tie (equal performance)";
}
