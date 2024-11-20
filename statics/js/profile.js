const fileInput = document.getElementById("choose-image");
const profilePic = document.getElementById("profile-pic");

// Listen for changes to the file input
fileInput.addEventListener("change", function () {
    // Check if any file is selected
    if (fileInput.files.length > 0) {
        // Get the selected file
        const selectedFile = fileInput.files[0];

        // Create a FileReader to read the selected file
        const reader = new FileReader();

        // Define a function to execute when the FileReader finishes loading
        reader.onload = function (e) {
            // Set the src attribute of the profile pic to the loaded image
            profilePic.src = e.target.result;
        };

        // Read the selected file as a data URL
        reader.readAsDataURL(selectedFile);
    }
});