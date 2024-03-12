const submitButton = document.getElementById("submit-button");
const loadingProgress = document.getElementById("loading-progress");
const linkContainer = document.getElementById("linkContainer");
let processingChunks = false

window.addEventListener("DOMContentLoaded", e => {
    document.getElementById("submit-form").addEventListener("submit", function(e) {
      e.preventDefault()
      const url = document.getElementById("textInput").value;
      
      if (isValidUrl(url)) {
        fetchDataChunks(url)
      }

      console.log("submit");
    });
});
async function fetchDataChunks(url) {
  submitButton.disabled = true;

  try {
    const csrfToken = getCSRFToken()

    const response = await fetch('/get_overall', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json', 'X-CSRFToken': csrfToken
      },
      body: JSON.stringify(url)
    })

    const reader = response.body.getReader();
    const decoder = new TextDecoder('utf-8');
  
    let chunk = '';

    while (true) {
      const { done, value } = await reader.read();
  
      if (done) {
        break;
      }
  
      chunk = decoder.decode(value, { stream: true });
  
      chunk_object = JSON.parse(chunk)
      
      // Process the chunked data here
      processDataChunk(chunk_object);
    }

    chunksProcessed()

  } catch (error) {
    console.log("Error: ", error)
    processingChunks = false
    submitButton.disabled = false;
  }
}

function processDataChunk(chunk) {
  if (!processingChunks) {
    linkContainer.innerHTML = ""
  }

  processingChunks = true

  if (chunk.data) {
    const { data } = chunk
    const { label, url } = data
    const ul = document.createElement("ul");
    var li = document.createElement("li"); // Create list item
    // Create anchor element
    var a = document.createElement("a");
    a.href = url; // Set href attribute
    a.textContent = url; // Set text content
    // Append Type and Link to the list item
    li.textContent = label + ": ";
    li.appendChild(a);
    // Append list item to the unordered list
    ul.appendChild(li);
    // Append the unordered list to the container element
    linkContainer.appendChild(ul);
  }

  if (chunk.progress) {
    const { progress } = chunk
    roundedProgress = Math.round(progress)
    loadingProgress.innerHTML = roundedProgress
  }

}

function chunksProcessed() {
  processingChunks = false
  submitButton.disabled = false;
}


function getCSRFToken() {
  var csrfToken = document.querySelector('meta[name="csrf-token"]');
  if (csrfToken) {
      return csrfToken.getAttribute('content');
  } else {
      console.error('CSRF token not found in meta tag');
      return null;
  }
}

function isValidUrl(url) {
  try { 
    return Boolean(new URL(url)); 
  }
  catch(e){ 
    return false; 
  }
}