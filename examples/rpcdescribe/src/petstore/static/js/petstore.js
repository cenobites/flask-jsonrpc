// RPC Describe Dashboard JavaScript

// Configuration
const API_ENDPOINT = '/api';
const API_VERSION = '2.0';

// Sample data for each method
const methodExamples = {
  'Petstore.get_pets': {
    tags: ['dog', 'cat'],
    limit: 10
  },
  'Petstore.create_pet': {
    new_pet: {
      name: 'Max',
      tag: 'dog'
    }
  },
  'Petstore.get_pet_by_id': {
    id: 1
  },
  'Petstore.delete_pet_by_id': {
    id: 1
  }
};

// Initialize the page
document.addEventListener('DOMContentLoaded', function() {
  console.log('RPC Describe Dashboard loaded');

  // Set up method selector
  const methodSelect = document.getElementById('method-select');
  if (methodSelect) {
    methodSelect.addEventListener('change', updateParamsForMethod);
    updateParamsForMethod(); // Set initial params
  }

  // Set up navigation
  setupNavigation();

  // Update pet count if available
  updatePetCount();
});

// Update navigation active state
function setupNavigation() {
  const navLinks = document.querySelectorAll('.nav-link');

  navLinks.forEach(link => {
    link.addEventListener('click', function(e) {
      if (this.getAttribute('href').startsWith('#')) {
        e.preventDefault();
        navLinks.forEach(l => l.classList.remove('active'));
        this.classList.add('active');

        const targetId = this.getAttribute('href').substring(1);
        scrollToSection(targetId);
      }
    });
  });

  // Update active link on scroll
  window.addEventListener('scroll', function() {
    const sections = document.querySelectorAll('section[id]');
    let current = '';

    sections.forEach(section => {
      const sectionTop = section.offsetTop;
      const sectionHeight = section.clientHeight;
      if (window.pageYOffset >= (sectionTop - 100)) {
        current = section.getAttribute('id');
      }
    });

    navLinks.forEach(link => {
      link.classList.remove('active');
      if (link.getAttribute('href') === `#${current}`) {
        link.classList.add('active');
      }
    });
  });
}

// Scroll to section
function scrollToSection(sectionId) {
  const element = document.getElementById(sectionId);
  if (element) {
    const offset = 80; // Header height
    const elementPosition = element.getBoundingClientRect().top;
    const offsetPosition = elementPosition + window.pageYOffset - offset;

    window.scrollTo({
      top: offsetPosition,
      behavior: 'smooth'
    });
  }
}

// Update parameters based on selected method
function updateParamsForMethod() {
  const methodSelect = document.getElementById('method-select');
  const paramsInput = document.getElementById('params-input');

  if (methodSelect && paramsInput) {
    const selectedMethod = methodSelect.value;
    const exampleParams = methodExamples[selectedMethod];

    if (exampleParams) {
      paramsInput.value = JSON.stringify(exampleParams, null, 2);
    }
  }
}

// Test a specific method
function testMethod(methodName) {
  const methodSelect = document.getElementById('method-select');
  const paramsInput = document.getElementById('params-input');

  if (methodSelect) {
    methodSelect.value = methodName;
    updateParamsForMethod();
  }

  scrollToSection('playground');
}

// Switch between tabs
function switchTab(tabName) {
  // Update buttons
  const tabButtons = document.querySelectorAll('.tab-btn');
  tabButtons.forEach(btn => btn.classList.remove('active'));
  event.target.classList.add('active');

  // Update content
  const tabContents = document.querySelectorAll('.tab-content');
  tabContents.forEach(content => content.classList.remove('active'));
  document.getElementById(`${tabName}-tab`).classList.add('active');
}

// Execute RPC request
async function executeRPC() {
  const methodSelect = document.getElementById('method-select');
  const paramsInput = document.getElementById('params-input');
  const responseOutput = document.getElementById('response-output');
  const requestOutput = document.getElementById('request-output');
  const statusIndicator = document.getElementById('status-indicator');
  const statusText = document.getElementById('status-text');

  // Get method and params
  const method = methodSelect.value;
  let params;

  try {
    params = paramsInput.value.trim() ? JSON.parse(paramsInput.value) : {};
  } catch (error) {
    showError('Invalid JSON in parameters', error.message);
    return;
  }

  // Build JSON-RPC request
  const requestId = generateRequestId();
  const requestBody = {
    jsonrpc: API_VERSION,
    method: method,
    params: params,
    id: requestId
  };

  // Show request
  requestOutput.innerHTML = `<code>${JSON.stringify(requestBody, null, 2)}</code>`;

  // Show loading state
  statusIndicator.className = 'status-badge loading';
  statusText.textContent = 'Sending request...';
  responseOutput.innerHTML = '<code>// Loading...</code>';

  try {
    // Send request
    const startTime = performance.now();
    const response = await fetch(API_ENDPOINT, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('jwt')}`
      },
      body: JSON.stringify(requestBody)
    });

    if (response.status === 401) {
      window.location.href = '/api/browse/login';
    }

    const endTime = performance.now();
    const duration = Math.round(endTime - startTime);

    // Parse response
    const data = await response.json();

    // Show response
    if (data.error) {
      showError('RPC Error', data.error, duration);
      responseOutput.innerHTML = `<code>${JSON.stringify(data, null, 2)}</code>`;
    } else {
      showSuccess('Success', duration);
      responseOutput.innerHTML = `<code>${JSON.stringify(data, null, 2)}</code>`;
    }

    // Update pet count if we modified data
    if (method.includes('create') || method.includes('delete')) {
      setTimeout(updatePetCount, 500);
    }

  } catch (error) {
    showError('Network Error', error.message);
    responseOutput.innerHTML = `<code>// Error: ${error.message}</code>`;
  }
}

// Show success status
function showSuccess(message, duration) {
  const statusIndicator = document.getElementById('status-indicator');
  const statusText = document.getElementById('status-text');

  statusIndicator.className = 'status-badge success';
  statusText.textContent = `${message} (${duration}ms)`;
}

// Show error status
function showError(title, message, duration) {
  const statusIndicator = document.getElementById('status-indicator');
  const statusText = document.getElementById('status-text');

  statusIndicator.className = 'status-badge error';
  statusText.textContent = duration ? `${title}: ${message} (${duration}ms)` : `${title}: ${message}`;
}

// Generate unique request ID
function generateRequestId() {
  return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
}

// Update pet count
async function updatePetCount() {
  try {
    const requestBody = {
      jsonrpc: API_VERSION,
      method: 'Petstore.get_pets',
      params: {},
      id: generateRequestId()
    };

    const response = await fetch(API_ENDPOINT, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('jwt')}`
      },
      body: JSON.stringify(requestBody)
    });

    if (response.status === 401) {
      window.location.href = '/api/browse/login';
    }

    const data = await response.json();

    if (data.error) {
      throw new Error(data.error.message);
    }

    if (data.result && Array.isArray(data.result)) {
      const totalPetsElement = document.getElementById('total-pets');
      if (totalPetsElement) {
        totalPetsElement.textContent = data.result.length;
      }
    }
  } catch (error) {
    console.error('Failed to update pet count:', error);
  }
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
  // Ctrl/Cmd + Enter to execute
  if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
    const paramsInput = document.getElementById('params-input');
    if (document.activeElement === paramsInput) {
      e.preventDefault();
      executeRPC();
    }
  }
});

// Export functions for global use
window.scrollToSection = scrollToSection;
window.testMethod = testMethod;
window.switchTab = switchTab;
window.executeRPC = executeRPC;
