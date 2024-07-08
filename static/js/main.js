// Define a function to encapsulate the jQuery code
function initializePage() {
    // Init
    $('.loader').hide();
    $('#selected-image').hide();
    $('#remove-btn').hide();
    $('#preview').hide(); // Hide the preview placeholder initially

    // Upload Preview
    function readURL(input) {
        if (input.files && input.files[0]) {    // if there is file selected
            var reader = new FileReader();
            reader.onload = function (e) {        // what happens when the file is read
                $('#selected-image').attr('src', e.target.result).show();
                $('#preview').show(); // Show the preview placeholder
                $('#btn-analyze').show(); // Show analyze button when image is uploaded
                $('#remove-btn').show(); // Show remove button when image is uploaded
                $('#drop-area div').hide(); // Hide drag & drop text
                $('#imageUpload').show();
            }
            reader.readAsDataURL(input.files[0]);   //reads the file as a data URL
        }
    }
    $("#imageUpload").change(function () {
        readURL(this);
    });

    // Drag over handler
    function dragOverHandler(event) {
        event.preventDefault();
        $('#drop-area').addClass('drag-over');
    }

    // Drop handler
    function dropHandler(event) {
        event.preventDefault();
        $('#drop-area').removeClass('drag-over');
        var files = event.originalEvent.dataTransfer.files;    // Get files that were dropped
        var input = $('#imageUpload')[0];
        input.files = files;

        readURL(input);
    }

    // Remove Image
    window.removeImage = function () {
        const fileInput = document.getElementById('imageUpload');
        fileInput.value = ''; // Clear the file input
        $('#selected-image').hide(); // Hide the selected image
        $('#preview').hide(); // Hide the preview placeholder
        $('#btn-analyze').show(); // Hide the analyze button
        $('#remove-btn').hide(); // Hide the remove button
        $('#drop-area div').show(); // Show drag & drop text
        $('#imageUpload').show(); // Show file input
    }

    // Attach event handlers
    $('#drop-area').on('dragover', dragOverHandler);
    $('#drop-area').on('drop', dropHandler);
    $('#remove-btn').click(removeImage); // Attach click event to the remove button using jQuery

    // Analyze
    $('form[name="sec1"]').submit(function (event) {
        event.preventDefault(); // Prevent form submission

        var form_data = new FormData($(this)[0]);

        // Show loading animation and hide the image
        $('#selected-image').show();
        $('#preview').show();
        $('#btn-analyze').hide();
        $('.loader').show();
        $('#imageUpload').show();

        // Determine the correct endpoint based on the current URL
        let endpoint;
        if (window.location.pathname.includes('sperm_analysis.html')) {
            endpoint = '/predict1';  // Endpoint for sperm analysis
        } else if (window.location.pathname.includes('embryo_analysis.html')) {
            endpoint = '/predict2';  // Endpoint for embryo analysis
        } else {
            alert("Invalid analysis type. Please navigate to the appropriate analysis page.");
            $('.loader').hide(); // Hide loader if invalid page
            return;
        }

        // Make prediction by calling the appropriate API endpoint
        $.ajax({
            type: 'POST',
            url: endpoint,
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                // Update prediction result and report content on the popup frame
                setTimeout(function () {
                    // Show the popup frame
                    $('#myModal').show();
                    // Handle prediction result based on analysis type
                    let notEntity = false;
                    if (window.location.pathname.includes('sperm_analysis.html')) {
                        // Check if prediction is "Bad Sperm" with >= 0.9999accuracy
                        if (data.prediction.toLowerCase() === 'bad sperm' && data.accuracy >= 0.9999) {
                            $('#prediction-result').text('Prediction Result: Not a sperm.'); // Display simplified message
                            $('#accuracy').text('Accuracy: ' + (data.accuracy * 100).toFixed(2) + '%');
                            notEntity = true;
                        }
                    } else if (window.location.pathname.includes('embryo_analysis.html')) {
                        // Check if prediction is "Bad Embryo" with accuracy above 80%
                        if (data.prediction.toLowerCase().includes('bad embryo') && data.accuracy > 0.8) {
                            $('#prediction-result').text('Prediction Result: Not an Embryo.'); // Display simplified message
                            $('#accuracy').text('Accuracy: ' + (data.accuracy * 100).toFixed(2) + '%');

                            notEntity = true;
                        }
                    }
                    // Update the popup content if not classified as "Not Sperm" or "Not Embryo"
                    if (!notEntity) {    // true
                        $('#prediction-result').text('Prediction Result: ' + data.prediction);
                        $('#accuracy').text('Accuracy: ' + (data.accuracy * 100).toFixed(2) + '%');
                    }
                    // Hide loader
                    $('.loader').hide();
                    console.log('Success!');
                }, 1000); // 1000 milliseconds = 1 sec
            },

            error: function (xhr, status, error) {
                // Handle error
                console.log('Error:', error);
                console.log('Status:', status);
                console.log('Response:', xhr.responseText);
                // Hide loader
                $('.loader').hide();
                // Optionally, show an error message to the user
                alert('An error occurred while processing your request. Please try again.');
            }
        });
    });
}
// Call initializePage function when document is ready
$(document).ready(function () {
    initializePage();
});

function closeModal() {
    $('#myModal').hide();
}
