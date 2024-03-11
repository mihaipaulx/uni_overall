window.addEventListener("DOMContentLoaded", e => {
  const socket = io({
      query: { debug: true }
  });

  // Check if the socket is connected before executing further code
  socket.on("connect", function() {
    // This function will execute once the socket connection is successful
    console.log("Socket connected successfully!");

    document.getElementById("submit-form").addEventListener("submit", function(e) {
      e.preventDefault()
      toggleEvent(socket);
    });

    socket.on("update_loading", function(loading_progress) {
      console.log(loading_progress + "%")
    })

    socket.on("overall_data", function(data) {
      console.log(data)
      var ul = document.createElement("ul");

      // Loop through the items array and create list items for each item
      for (const [label, url] of data) {
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

          // Get the container element where the list will be appended
          var container = document.getElementById("linkContainer");

          // Clear container content
          container.innerHTML = "";

          // Append the unordered list to the container element
          container.appendChild(ul);
      }

      var submitButton = document.getElementById("submit-button");
      submitButton.disabled = false;
    });
  });

  // Error handling for connection failure
  socket.on("connect_error", function(error) {
    console.error("Socket connection failed:", error);
  });

  socket.on("disconnect", function(reason) {
      console.log("Socket disconnected, reason: ", reason);
  });
});

function toggleEvent(socket) {
  var prevURL = "";
  var currentURL = document.getElementById("textInput").value;
  var submitButton = document.getElementById("submit-button");
  if (currentURL !== "" && currentURL !== prevURL) {
      submitButton.disabled = true;
      socket.emit('submit', currentURL);
      console.log("submit");
      prevURL = currentURL
  }
}