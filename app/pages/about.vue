<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-yellow-50">
    <!-- Header -->
    <header class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-4">
            <div class="bg-blue-500 text-white p-2 rounded-lg">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
              </svg>
            </div>
            <h1 class="text-2xl font-bold text-gray-900">Swarm Lab</h1>
          </div>
          <nav class="flex space-x-4">
            <NuxtLink to="/dashboard" class="text-gray-600 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium">
              Dashboard
            </NuxtLink>
            <NuxtLink to="/about" class="text-blue-600 bg-blue-50 px-3 py-2 rounded-md text-sm font-medium">
              About
            </NuxtLink>
          </nav>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <!-- Hero Section -->
      <div class="text-center mb-12">
        <div class="bg-blue-500 text-white w-24 h-24 rounded-full mx-auto mb-6 flex items-center justify-center">
          <svg class="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
          </svg>
        </div>
        <h1 class="text-4xl font-bold text-gray-900 mb-4">About Swarm Lab</h1>
        <p class="text-xl text-gray-600 max-w-2xl mx-auto">
          An educational web application for swarm intelligence algorithm research and simulation
        </p>
      </div>

      <!-- Project Information -->
      <div class="bg-white rounded-xl shadow-lg p-8 mb-8">
        <h2 class="text-2xl font-bold text-gray-900 mb-6">Project Overview</h2>
        <div class="space-y-4 text-gray-700">
          <p>
            Swarm Lab is a comprehensive educational platform designed to facilitate the study and experimentation 
            of swarm intelligence algorithms. Built with modern web technologies, it provides an intuitive interface 
            for researchers and students to simulate, analyze, and understand the behavior of various swarm algorithms.
          </p>
          <p>
            The platform supports both Ant Colony Optimization (ACO) and Particle Swarm Optimization (PSO) algorithms, 
            offering real-time visualization, parameter tuning capabilities, and performance tracking features that make 
            complex algorithm concepts more accessible to learners.
          </p>
        </div>
      </div>

      <!-- Creator Information -->
      <div class="bg-white rounded-xl shadow-lg p-8 mb-8">
        <h2 class="text-2xl font-bold text-gray-900 mb-6">Project Details</h2>
        <div class="grid md:grid-cols-2 gap-8">
          <div>
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Creator Information</h3>
            <div class="space-y-3">
              <div class="flex items-center space-x-3">
                <div class="bg-blue-100 p-2 rounded-lg">
                  <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                </div>
                <div>
                  <p class="text-sm text-gray-500">Created by</p>
                  <p class="font-medium text-gray-900">Muhammad Faza Abiyyu</p>
                </div>
              </div>
              <div class="flex items-center space-x-3">
                <div class="bg-yellow-100 p-2 rounded-lg">
                  <svg class="w-5 h-5 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 19 16.5 19c-1.746 0-3.332.477-4.5 1.253" />
                  </svg>
                </div>
                <div>
                  <p class="text-sm text-gray-500">Academic Purpose</p>
                  <p class="font-medium text-gray-900">Tugas Akhir Sarjana 1</p>
                </div>
              </div>
              <div class="flex items-center space-x-3">
                <div class="bg-green-100 p-2 rounded-lg">
                  <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                  </svg>
                </div>
                <div>
                  <p class="text-sm text-gray-500">Institution</p>
                  <p class="font-medium text-gray-900">Telkom University Purwokerto</p>
                </div>
              </div>
            </div>
          </div>
          
          <div>
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Technical Specifications</h3>
            <div class="space-y-3">
              <div class="flex items-center space-x-3">
                <div class="bg-purple-100 p-2 rounded-lg">
                  <svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
                  </svg>
                </div>
                <div>
                  <p class="text-sm text-gray-500">Frontend Framework</p>
                  <p class="font-medium text-gray-900">Nuxt 4</p>
                </div>
              </div>
              <div class="flex items-center space-x-3">
                <div class="bg-indigo-100 p-2 rounded-lg">
                  <svg class="w-5 h-5 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zM21 5a2 2 0 00-2-2h-4a2 2 0 00-2 2v12a4 4 0 004 4h4a2 2 0 002-2V5z" />
                  </svg>
                </div>
                <div>
                  <p class="text-sm text-gray-500">Styling</p>
                  <p class="font-medium text-gray-900">Tailwind CSS</p>
                </div>
              </div>
              <div class="flex items-center space-x-3">
                <div class="bg-red-100 p-2 rounded-lg">
                  <svg class="w-5 h-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                  </svg>
                </div>
                <div>
                  <p class="text-sm text-gray-500">License</p>
                  <p class="font-medium text-gray-900">MIT License</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Features -->
      <div class="bg-white rounded-xl shadow-lg p-8 mb-8">
        <h2 class="text-2xl font-bold text-gray-900 mb-6">Key Features</h2>
        <div class="grid md:grid-cols-2 gap-6">
          <div class="flex items-start space-x-4">
            <div class="bg-blue-100 p-3 rounded-lg">
              <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <div>
              <h3 class="font-semibold text-gray-900 mb-1">Real-time Visualization</h3>
              <p class="text-gray-600 text-sm">Watch algorithm performance metrics update in real-time with interactive charts and graphs.</p>
            </div>
          </div>
          
          <div class="flex items-start space-x-4">
            <div class="bg-green-100 p-3 rounded-lg">
              <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4" />
              </svg>
            </div>
            <div>
              <h3 class="font-semibold text-gray-900 mb-1">Parameter Tuning</h3>
              <p class="text-gray-600 text-sm">Fine-tune algorithm parameters directly through an intuitive table interface for optimal performance.</p>
            </div>
          </div>
          
          <div class="flex items-start space-x-4">
            <div class="bg-purple-100 p-3 rounded-lg">
              <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4" />
              </svg>
            </div>
            <div>
              <h3 class="font-semibold text-gray-900 mb-1">Data Management</h3>
              <p class="text-gray-600 text-sm">Import/export data in JSON and CSV formats with full CRUD operations support.</p>
            </div>
          </div>
          
          <div class="flex items-start space-x-4">
            <div class="bg-yellow-100 p-3 rounded-lg">
              <svg class="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
            </div>
            <div>
              <h3 class="font-semibold text-gray-900 mb-1">Educational Focus</h3>
              <p class="text-gray-600 text-sm">Designed specifically for educational use with clear instructions and intuitive user interface.</p>
            </div>
          </div>
        </div>
      </div>

      <!-- GitHub Repository -->
      <div class="bg-white rounded-xl shadow-lg p-8 text-center">
        <h2 class="text-2xl font-bold text-gray-900 mb-4">Open Source Project</h2>
        <p class="text-gray-600 mb-6">
          This project is open source and available under the MIT License. 
          Feel free to contribute, use, or modify according to your needs.
        </p>
        <a 
          href="https://github.com/fazza-abiyyu/swarm-lab" 
          target="_blank" 
          rel="noopener noreferrer"
          class="inline-flex items-center px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors duration-200"
        >
          <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
          </svg>
          View on GitHub
        </a>
      </div>
    </main>

    <!-- Footer -->
    <footer class="bg-white border-t border-gray-200 mt-16">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div class="text-center">
          <p class="text-gray-600">
            © 2024 Swarm Lab. Built with ❤️ for educational purposes.
          </p>
          <p class="text-sm text-gray-500 mt-2">
            Telkom University Purwokerto - Tugas Akhir Sarjana 1
          </p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
useHead({
  title: 'About - Swarm Lab',
  meta: [
    {
      name: 'description',
      content: 'Learn about Swarm Lab - an educational web application for swarm intelligence algorithm research and simulation by Muhammad Faza Abiyyu'
    }
  ]
})
</script>