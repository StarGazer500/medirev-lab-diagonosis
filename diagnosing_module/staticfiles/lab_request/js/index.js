$(document).ready(function() {
    function createModal(bodyContent) {
        // Remove any existing modal with the same ID first
        $('#dynamicModal').remove();
        
        // Modal HTML structure with dynamic body content - Updated for Bootstrap 5
        var modalHTML = `
          <div class="modal fade" id="dynamicModal" tabindex="-1" aria-labelledby="dynamicModalLabel" aria-hidden="true">
            <div class="modal-dialog">
              <div class="modal-content">
                <div class="modal-header">
                  <h5 class="modal-title" id="dynamicModalLabel">Notification</h5>
                  <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                  ${bodyContent}
                </div>
                <div class="modal-footer">
                  <button type="button" class="btn btn-secondary" id="hideModal" data-bs-dismiss="modal">Close</button>
                </div>
              </div>
            </div>
          </div>
        `;
        
        // Append the modal HTML directly to the body
        $('body').append(modalHTML);
        
        // Initialize the modal
        var modalElement = document.getElementById('dynamicModal');
        var modalInstance = new bootstrap.Modal(modalElement);
        
        // Handle the close button click
        $('#hideModal').click(function() {
            modalInstance.hide();
        });
        
        // Clean up modal when hidden
        $(modalElement).on('hidden.bs.modal', function () {
            $(this).remove();
        });
        
        return modalInstance;
    }
    
    // Get CSRF token from cookie
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    const csrftoken = getCookie('csrftoken');
    
    // Function to collect form data
    function collectFormData() {
        var formData = {
            first_name: $('#first-name').val().trim(),
            last_name: $('#last-name').val().trim(),
            email: $('#email').val().trim(),
            date_of_birth: $('#birth-date').val().trim(),
            gender: $('#gender').val(),
            contact_number: $('#mobile').val().trim(),
            test_description: $('#message').val().trim(),
            requested_date: new Date().toISOString() // Adding the current date as requested_date
        };
        return formData;
    }
    
    // Submit button click event
    $('#submit-btn').on('click', function() {
        console.log("csrf", csrftoken);
        var formData = collectFormData();
        
        // Check if all required fields are filled
        if (!formData.first_name || !formData.last_name || !formData.email || 
            !formData.date_of_birth || !formData.gender || !formData.contact_number || 
            !formData.test_description) {
            var modal = createModal("Please fill all required fields before submitting.");
            modal.show();
            return;
        }
        
        // Perform AJAX request to submit the data to the server
        $.ajax({
            url: '/laboratory/create-laborder-request/',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(formData),
            headers: {
                'X-CSRFToken': csrftoken
            },
            timeout: 15000, // 15 seconds timeout
            success: function(response) {
                console.log("Response:", response);
                
                var modal = createModal("Appointment submitted successfully.An appointment date will be forwarded in your email in short time!");
                modal.show();
                
                // Clear form on success
               
            },
            error: function(xhr, status, error) {
                console.log("Error status:", status);
                console.log("Error details:", error);
                
                var errorMessage = 'An error occurred.';
                
                // Try to get error message from response
                if (xhr.responseJSON && xhr.responseJSON.message) {
                    errorMessage = xhr.responseJSON.message;
                }
                
                // Handle different error types
                if (status === 'timeout') {
                    errorMessage = "Request timed out. Please check your internet connection and try again.";
                } else if (status === 'error' && xhr.status === 0) {
                    errorMessage = "Cannot connect to the server. Please check your internet connection.";
                } else if (xhr.status === 400) {
                    errorMessage = xhr.responseJSON && xhr.responseJSON.message 
                    ? xhr.responseJSON.message 
                    : "Validation error occurred. Please check your input.";
                } else if (xhr.status === 500) {
                    errorMessage = xhr.responseJSON && xhr.responseJSON.message 
                    ? xhr.responseJSON.message 
                    : "Some Unkwowinlu happened. Try again, if the issure persist, we will resole it soon.";
                }
                
                var modal = createModal(errorMessage);
                modal.show();
            }
        });
    });
});