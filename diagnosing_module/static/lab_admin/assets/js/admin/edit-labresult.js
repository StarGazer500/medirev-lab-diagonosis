$(document).ready(function() {
    // Function to fetch patient data from the server

     // Get CSRF token from cookie
     function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

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
    
    
    function fetchLabResultData() {
        // let id = 1; // Replace with the actual patient ID if need
        // ed
        
        let labresultId= localStorage.getItem('labresultId');
        $.ajax({
            url: `/laboratory/get-lab-result/${labresultId}`, // Replace with your actual endpoint
            type: 'GET',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            success: function(response) {
                // Check if response has data
                if (response) {
                    console.log(response)
                    // Call the function to populate the patient data
                    populateLabResultData(response);
                } else {
                    // Show message if no patient data found
                    $('#labrequest-info-row').html('<div class="col-12 text-center">No Lab records found</div>');
                }
            },
            error: function(xhr, status, error) {
                console.log("Error fetching Lab Results data:", error);
                
                var errorMessage = 'Failed to load Lab Result data.';
                if (xhr.responseJSON && xhr.responseJSON.message) {
                    errorMessage = xhr.responseJSON.message;
                }
                
                var modal = createModal(errorMessage);
                modal.show();
            }
        });
    }

    // Function to populate patient data into the div
    function populateLabResultData(labresult) {
        const labrequestDataHtml = `
            <div class="col-lg-8 offset-lg-2">
        <form id="labresultForm">
            <div class="row">
                <!-- Result Id -->
                <div class="col-sm-6">
                    <div class="form-group">
                        <label>Result ID</label>
                        <input class="form-control" name="id" type="text" value="${labresult.id}" readonly>
                    </div>
                </div>

               
               
              <!-- Lab Results -->
            <div class="col-sm-6">
                <div class="form-group">
                    <label>Lab Results</label>
                    <textarea class="form-control" id="message" name="result">${labresult.result}</textarea>
                </div>
            </div>

           <!-- Submit Button -->
                <div class="col-sm-12">
                    <div class="form-group text-center">
                        <button type="submit" class="btn btn-primary submit-btn">Save</button>
                    </div>
                </div>
                
            </div>
        </form>
    </div>
        `;
        
        $('#labresult-info-row').html(labrequestDataHtml);

        // Add form submission handler
        $('#labresultForm').on('submit', function(e) {
            e.preventDefault(); // Prevent default form submission
            
            let labresultId= localStorage.getItem('labresultId');
            let formData = {
    
                
                result: $('#message').val().trim()
            };

            $.ajax({
                url: `/laboratory/get-lab-result/${labresultId}/`, // Adjust the endpoint as needed
                type: 'PUT',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                },
                data: JSON.stringify(formData),
                success: function(response) {
                    var modal = createModal('Lab Result updated successfully!');
                    modal.show();
                    
                    // Optionally refresh the data after update
                    fetchLabRequestData();
                },
                error: function(xhr, status, error) {
                    console.log("Error updating Lab Result data:", error);
                    
                    var errorMessage = 'Failed to update Lab Result data.';
                    if (xhr.responseJSON && xhr.responseJSON.message) {
                        errorMessage = xhr.responseJSON.message;
                    }
                    
                    var modal = createModal(errorMessage);
                    modal.show();
                }
            });
        });
    }
    // Fetch patient data on page load
    fetchLabResultData();
});
