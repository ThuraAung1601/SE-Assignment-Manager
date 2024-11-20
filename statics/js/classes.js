document.getElementById('changeIndexButton').addEventListener('click', function() {
    // Get the current index
    var currentIndex = parseInt('{{ current_index }}');

    // Increment the index (replace this logic with your desired index change)
    var newIndex = currentIndex + 1;

    // Update the URL or perform any other action with the new index
    window.location.href = '/your-path?index=' + newIndex;
});