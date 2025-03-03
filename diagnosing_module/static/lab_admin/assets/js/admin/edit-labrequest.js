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
    
    
    function fetchLabRequestData() {
        // let id = 1; // Replace with the actual patient ID if need
        // ed
        
        let labrequestId = localStorage.getItem('labrequestId');
        $.ajax({
            url: `/laboratory/get-laborder-request/${labrequestId}`, // Replace with your actual endpoint
            type: 'GET',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            success: function(response) {
                // Check if response has data
                if (response) {
                    console.log(response)
                    // Call the function to populate the patient data
                    populateLabRequestData(response);
                } else {
                    // Show message if no patient data found
                    $('#labrequest-info-row').html('<div class="col-12 text-center">No Lab Appointment records found</div>');
                }
            },
            error: function(xhr, status, error) {
                console.log("Error fetching Appointment data:", error);
                
                var errorMessage = 'Failed to load Appointment data.';
                if (xhr.responseJSON && xhr.responseJSON.message) {
                    errorMessage = xhr.responseJSON.message;
                }
                
                var modal = createModal(errorMessage);
                modal.show();
            }
        });
    }

    // Function to populate patient data into the div
    function populateLabRequestData(labrequest) {
        const labrequestDataHtml = `
            <div class="col-lg-8 offset-lg-2">
        <form id="labrequestForm">
            <div class="row">
                <!-- Appointment Id -->
                <div class="col-sm-6">
                    <div class="form-group">
                        <label>Appointment ID</label>
                        <input class="form-control" name="id" type="text" value="${labrequest.id}" readonly>
                    </div>
                </div>

                <!-- Patient Name -->
                <div class="col-sm-6">
                    <div class="form-group">
                        <label>Patient Name</label>
                        <input class="form-control" name="patient" type="text" value="${labrequest.patient}" readonly>
                    </div>
                </div>

                <!-- Appointment Status -->
                <div class="col-sm-6">
                    <div class="form-group">
                        <label>Appointment Status</label>
                        <select class="form-control" id ="statusSelect" name="status">
                            <option value="PENDING" ${labrequest.status === 'PENDING' ? 'selected' : ''}>PENDING</option>
                            <option value="COMPLETED" ${labrequest.status === 'COMPLETED' ? 'selected' : ''}>COMPLETED</option>
                            <option value="CANCELLED" ${labrequest.status === 'CANCELLED' ? 'selected' : ''}>CANCELLED</option>
                        </select>
                    </div>
                </div>


             
               

                <!-- Requested Date -->
                <div class="col-sm-6">
                    <div class="form-group">
                        <label>Requested Date</label>
                        <input class="form-control" name="requested_date" type="date" value="${labrequest.requested_date}" readonly>
                    </div>
                </div>

                 <!-- Order Date -->
                <div class="col-sm-6">
                    <div class="form-group">
                        <label>Order Date</label>
                        <input class="form-control" name="order_date" type="date" value="${labrequest.order_date}" readonly>
                    </div>
                </div>

               
              <!-- Test Description -->
            <div class="col-sm-6">
                <div class="form-group">
                    <label>Test Description</label>
                    <textarea class="form-control" id="message" name="test_description">${labrequest.test_description}</textarea>
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
        
        $('#labrequest-info-row').html(labrequestDataHtml);

        // Add form submission handler
        $('#labrequestForm').on('submit', function(e) {
            e.preventDefault(); // Prevent default form submission
            
            let labrequestId= localStorage.getItem('labrequestId');
            let formData = {
    
                
                request_status:  $('#statusSelect').val(),
                test_description: $('#message').val().trim()
            };

            $.ajax({
                url: `/laboratory/get-laborder-request/${labrequestId}/`, // Adjust the endpoint as needed
                type: 'PUT',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                },
                data: JSON.stringify(formData),
                success: function(response) {
                    var modal = createModal('Appointment data updated successfully!');
                    modal.show();
                    
                    // Optionally refresh the data after update
                    fetchLabRequestData();
                },
                error: function(xhr, status, error) {
                    console.log("Error updating appointment data:", error);
                    
                    var errorMessage = 'Failed to update Appointment data.';
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
    fetchLabRequestData();
});
