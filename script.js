    // Add your JavaScript code here
    document.addEventListener('DOMContentLoaded', () => {
      const lines = document.querySelectorAll('.code-container .line');
      
      function animateLine(index) {
          // Add the active class to the line
          lines[index].classList.add('active');
      
          // Remove the active class from the line after a delay
          setTimeout(() => {
          lines[index].classList.remove('active');
      
          // Call the function again with the next line index
          animateLine((index + 1) % lines.length);
          }, 500);
      }
      
      // Start the animation by calling the function with the first line index
      animateLine(0);
       
  });