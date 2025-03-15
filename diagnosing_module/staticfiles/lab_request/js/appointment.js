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
                localStorage.setItem("id",response.id)
                
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




      // Function to fetch lab request data from the server
      function fetchLabRequestData() {
        let labrequestId = localStorage.getItem("id")
    
        console.log("id",labrequestId)
        $.ajax({
            url: `/laboratory/get-laborder-request/${labrequestId}/`,
            type: 'GET',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            success: function(response) {
                // Clear existing table rows
                $('#labrequest-tbody').empty();
                console.log("res1",response)
                
                // Check if response has data
                if (response && response.length > 0) {
                

                    
                    // Append each lab request to the table
                    $.each(response, function(index, labrequest) {
                        appendLabRequestToTable(labrequest);
                    });
                } else if(response && response.length ===undefined){
                  appendLabRequestToTable(response);
                
                }else {
                    // Show message if no lab requests
                    $('#labrequest-tbody').append('<tr><td colspan="7" class="text-center">No Lab Request records found</td></tr>');
                }
            },
            error: function(xhr, status, error) {
                console.log("Error fetching Lab Request data:", error);
                
                var errorMessage = 'Failed to load Lab Request data.';
                if (xhr.responseJSON && xhr.responseJSON.message) {
                    errorMessage = xhr.responseJSON.message;
                }
                
                var modal = createModal(errorMessage);
                modal.show();
            }
        });
    }
    
    // Function to append a single lab request to the table
    function appendLabRequestToTable(labrequest) {
        // Format dates (assuming date is in ISO format)
        let formattedOrderDate = formatDate(labrequest.order_date);
        let formattedRequestDate = formatDate(labrequest.requested_date);
        
        // Create table row with lab request data
        var labrequestRow = `
            <tr data-labrequest-id="${labrequest.id}">
                <td>${labrequest.id}</td>
                <td>${labrequest.patient}</td>
                <td>${labrequest.test_description}</td>
                <td>${formattedOrderDate}</td>
                <td>${formattedRequestDate}</td>
                <td>${labrequest.status}</td>
                
            </tr>
        `;
        
        // Append the row to the table body
        $('#labrequest-tbody').append(labrequestRow);

    }

   
    // Prevent default behavior of the action links
$(document).on('click', '.dropdown-item', function(e) {
    e.preventDefault(); // Prevents scrolling up behavior

    var action = $(this).text().toLowerCase();
    var labrequestId = $(this).closest('tr').data('labrequest-id'); // Get the lab request ID from the row

    if (action === 'edit') {
        // Perform the edit action, for example, redirect to edit page
        // window.location.href = `/laboratory/edit-appointment/${labrequestId}/`;
    } 
});



 


    $(document).on('click', '.edit-labrequest-btn', function(event) {
        event.preventDefault(); // Prevent default action (navigation)
       
    
        // Get the parent row of the clicked Edit button
        var labrequestRow = $(this).closest('tr');
        // console.log("patient email",patientRow)
        
        // Extract the email and other necessary information from the row
        // var patientEmail = patientRow.data('patient-email');
        // console.log(patientEmail)
        var labrequestId =labrequestRow.data('labrequest-id');
        console.log("id",labrequestId)
        
        // For now, log the email (you can store it in localStorage, sessionStorage, or use it directly)
        // console.log("Patient Email:", patientEmail);
        // console.log("Patient ID:", patientId);
    
        // Store the email in localStorage (or sessionStorage) if needed
        // localStorage.setItem('patientEmail', patientEmail);
        localStorage.setItem('labrequestId', labrequestId);

        // console.log("patient email",patientEmail)
    
    
        // Redirect to the Edit page or do something else
        window.location.href = `/laboratory/edit-appointment/`;
    });
    
    
    // Helper function to format date (YYYY-MM-DD to DD-MM-YY)
    function formatDate(dateString) {
        if (!dateString) return 'N/A';
        
        const date = new Date(dateString);
        if (isNaN(date.getTime())) return dateString; // Return original if invalid
        
        const day = String(date.getDate()).padStart(2, '0');
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const year = String(date.getFullYear()).slice(-2);
        
        return `${day}-${month}-${year}`;
    }
    
  
    
    // Delete lab request handler (using event delegation)
    $(document).on('click', '.delete-labrequest-btn', function(e) {
        e.preventDefault();
        const labrequestId = $(this).data('labrequest-id');
        
        // Show confirmation modal
        var modal = createModal(`Are you sure you want to delete this Lab Request record? <br><br>
            <div class="text-center">
                <button type="button" class="btn btn-danger" id="confirmDelete" data-id="${labrequestId}">Delete</button>
                <button type="button" class="btn btn-secondary ms-2" data-bs-dismiss="modal">Cancel</button>
            </div>`);
        modal.show();
        
        // Handle confirm delete button
        $('#confirmDelete').click(function() {
            const id = $(this).data('id');
            
            $.ajax({
                url: `/laboratory/get-laborder-request/${id}/`,
                type: 'DELETE',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                },
                success: function(response) {
                    modal.hide();

                    $('#dynamicModal').modal('dispose');
                    $('.modal-backdrop').remove();
                    $('body').removeClass('modal-open');
                    $('body').css('padding-right', '');
                    
                    // Show success message
                    var successModal = createModal("Lab Request record deleted successfully.");
                    successModal.show();

                    $('#dynamicModal').on('hidden.bs.modal', function() {
                        $('.modal-backdrop').remove();
                        $('body').removeClass('modal-open');
                        $('body').css('padding-right', '');
                        $(this).remove();
                    });
                        
                    
                    // Refresh lab request list
                    fetchLabRequestData();
                },
                error: function(xhr, status, error) {
                    console.log("Error deleting Lab Request:", error);
                    
                    var errorMessage = 'Failed to delete Lab Request record.';
                    if (xhr.responseJSON && xhr.responseJSON.message) {
                        errorMessage = xhr.responseJSON.message;
                    }
                    
                    modal.hide();
                    var errorModal = createModal(errorMessage);
                    errorModal.show();
                }
            });
        });
    });
    

   
    
    // Initial load of lab request data
    fetchLabRequestData();
});