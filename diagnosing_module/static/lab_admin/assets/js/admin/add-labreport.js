// Add form submission handler

$(document).ready(function() {
    
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
        console.log("lab results",labresultId)
        $.ajax({
            url: `/laboratory/get-lab-result/${labresultId}/`, // Replace with your actual endpoint
            type: 'GET',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            success: function(response) {
                // Check if response has data
                if (response) {
                    console.log(response)
                    // Call the function to populate the patient data
                    // populatePatientData(response);
                    $('input[name="lab_result_id"]').val(response.id);
                    fetchLabDoctorsData()
                  
                } 
            },
            error: function(xhr, status, error) {
                console.log("Error fetching Result data:", error);
                
                var errorMessage = 'Failed to load Result data.';
                if (xhr.responseJSON && xhr.responseJSON.message) {
                    errorMessage = xhr.responseJSON.message;
                    console.log(errorMessage)
                }
                
                // var modal = createModal(errorMessage);
                // modal.show();
            }
        });
    }

    // window.location.href = `/laboratory/add-appointment/`;
    let source_url = localStorage.getItem("source_url")
    // fetchPatientData()
    console.log(source_url)
   
    source_url==="http://localhost:8000/laboratory/lab-results/" ? fetchLabResultData() : fetchLabDoctorsData()

    function fetchLabDoctorsData() {
        $.ajax({
            url: `/laboratory/get-all-doctor/`, // Replace with your actual endpoint
            type: 'GET',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            success: function(response) {
                // Check if the response contains doctor data
                if (response && response.length > 0) {
                    console.log(response);
    
                    // Get the dropdown element
                    let $doctorDropdown = $('#doctorDropdown');
    
                    // Clear any existing options
                    $doctorDropdown.empty();
    
                    // Add a default 'Select a doctor' option
                    $doctorDropdown.append('<option value="">Select a doctor</option>');
    
                    // Loop through each doctor in the response and add them to the dropdown
                    response.forEach(function(doctor) {
                        let option = `<option value="${doctor.id}">${doctor.first_name} ${doctor.last_name}</option>`;
                        $doctorDropdown.append(option);
                    });
    
                    // Show the dropdown container
                    $('#doctorDropdownContainer').show();
                } else {
                    console.log("No doctors found.");
                    $('#doctorDropdownContainer').hide(); // Hide the dropdown if no doctors found
                }
            },
            error: function(xhr, status, error) {
                console.log("Error fetching Doctor data:", error);
    
                var errorMessage = 'Failed to load Doctor data.';
                if (xhr.responseJSON && xhr.responseJSON.message) {
                    errorMessage = xhr.responseJSON.message;
                    console.log(errorMessage);
                }
    
                var modal = createModal(errorMessage);
                modal.show();
            }
        });
    }
    
    // Event listener for the 'Shared With Doctor' checkbox
   
    

    $('#labreportForm').on('submit', function(e) {
        e.preventDefault(); // Prevent default form submission
        
        // let patientId = localStorage.getItem('patientId');
        let formData = {
            lab_result_id: $('input[name="lab_result_id"]').val(),
            report_data : $('textarea[name="report_data"]').val().trim(),
            shared_with_doctor: $('input[name="shared_with_doctor"]').prop('checked'),
            doctor_id: $('#doctorDropdown').val() 
            
        };
    
        $.ajax({
            url: `/laboratory/create-lab-report/`, // Adjust the endpoint as needed
            type: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            },
            data: JSON.stringify(formData),
            success: function(response) {
                var modal = createModal("Lab Report  submitted successfully.An appointment date will be forwarded in your email in short time!");
                modal.show();
                
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

})
