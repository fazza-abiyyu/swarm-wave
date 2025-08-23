# AI Chat Assistant Setup Guide

## Overview
The Swarm Lab application now includes an Interactive AI Chat Assistant powered by Google's Gemini API. This assistant helps users analyze simulation results, compare algorithm performance, and gain insights about swarm intelligence optimization.

## Features
- **Real-time chat** with AI assistant
- **Multi-language support** (English, Indonesian, Chinese)
- **Context-aware responses** based on simulation results
- **Secure API key handling** via environment variables
- **Persistent chat history** during session
- **Clean, responsive UI** with dark mode support

## Setup Instructions

### 1. Get Your Gemini API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the generated key

### 2. Configure Environment Variables
1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file and add your API key:
   ```bash
   # Gemini API Configuration
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   ```

3. **Important**: Never commit your `.env` file to version control. It's already included in `.gitignore`.

### 3. Verify Installation
The AI Chat Assistant is automatically integrated into the Simulation Page. After running simulations with both ACO and PSO algorithms, you'll see the AI Chat section below the "Overall Best Result" table.

## Usage Guide

### Starting a Conversation
1. **Run simulations** with both ACO and PSO algorithms
2. **Navigate** to the Simulation page
3. **Find** the AI Chat Assistant section below the results table
4. **Select** your preferred language from the dropdown
5. **Type** your question in the text area
6. **Click** "Send" or press Enter to submit

### Example Questions
- "Which algorithm performed better and why?"
- "Can you explain the load balancing index?"
- "What factors affect the makespan in ACO?"
- "Compare the convergence speed of both algorithms"
- "Suggest optimal parameters for my task set"

### Features
- **Language Selector**: Choose between English, Indonesian, or Chinese
- **Typing Indicator**: Shows "AI is thinking..." while processing
- **Error Handling**: Displays clear error messages if API calls fail
- **Clear Chat**: Reset conversation with the "Clear" button
- **Responsive Design**: Works on desktop and mobile devices

### Chat Interface
- **User messages**: Blue bubbles aligned to the right
- **AI responses**: Gray bubbles aligned to the left
- **Scrollable history**: View entire conversation
- **Auto-scroll**: New messages appear automatically

## Technical Details

### Architecture
- **Frontend-only**: No backend endpoints required
- **Composable pattern**: `useAiChat.ts` in `composables/` directory
- **Environment variables**: Secure API key management
- **Fetch API**: Direct Gemini API calls from client

### API Integration
- **Endpoint**: `https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent`
- **Context injection**: Simulation results automatically included
- **System prompt**: Pre-configured assistant behavior
- **Rate limiting**: Built-in request handling

### Security
- **No API key exposure**: Key only used server-side via environment variables
- **Frontend isolation**: API calls made through secure composable
- **No sensitive data**: Only simulation results are shared

## Troubleshooting

### Common Issues

1. **"Invalid API key" error**
   - Verify your `GEMINI_API_KEY` in `.env` file
   - Ensure the key has proper permissions
   - Check for typos or extra spaces

2. **AI Chat not appearing**
   - Ensure both ACO and PSO simulations are completed
   - Check browser console for errors
   - Verify the `.env` file exists and is properly formatted

3. **Language not changing**
   - Refresh the page after changing language
   - Check if the language selector is properly bound

### Debug Steps
1. **Check console**: Open browser DevTools → Console tab
2. **Verify API key**: Ensure `GEMINI_API_KEY` is set in `.env`
3. **Test connection**: Try a simple query to verify API access
4. **Check network**: Monitor API calls in Network tab

## Development Notes

### Adding New Languages
To add support for additional languages:
1. Update the language selector in `SimulationPage.vue`
2. Add language option to the `aiLanguage` ref
3. Test with sample queries in the new language

### Customizing System Prompt
Modify the system prompt in `composables/useAiChat.ts` to change AI behavior:
```typescript
const systemPrompt = `You are an AI assistant for Swarm Lab...`
```

### Extending Context
To include additional simulation data in AI context, modify the `sendMessage` function in `useAiChat.ts` to include more parameters from the simulation results.

## Support
For issues or questions about the AI Chat Assistant:
1. Check this setup guide
2. Review browser console for errors
3. Verify API key configuration
4. Test with different queries to isolate issues