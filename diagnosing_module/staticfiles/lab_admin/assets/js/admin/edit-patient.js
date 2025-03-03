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
    
    
    function fetchPatientData() {
        // let id = 1; // Replace with the actual patient ID if need
        // ed
        
        let patientId = localStorage.getItem('patientId');
        $.ajax({
            url: `/laboratory/get-patient/${patientId}`, // Replace with your actual endpoint
            type: 'GET',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            success: function(response) {
                // Check if response has data
                if (response) {
                    console.log(response)
                    // Call the function to populate the patient data
                    populatePatientData(response);
                } else {
                    // Show message if no patient data found
                    $('#patient-info-row').html('<div class="col-12 text-center">No patient records found</div>');
                }
            },
            error: function(xhr, status, error) {
                console.log("Error fetching patient data:", error);
                
                var errorMessage = 'Failed to load patient data.';
                if (xhr.responseJSON && xhr.responseJSON.message) {
                    errorMessage = xhr.responseJSON.message;
                }
                
                var modal = createModal(errorMessage);
                modal.show();
            }
        });
    }

    // Function to populate patient data into the div
    function populatePatientData(patient) {
        const patientDataHtml = `
            <div class="col-lg-8 offset-lg-2">
        <form id="patientForm">
            <div class="row">
                <!-- First Name -->
                <div class="col-sm-6">
                    <div class="form-group">
                        <label>First Name</label>
                        <input class="form-control" name="first_name" type="text" value="${patient.first_name}">
                    </div>
                </div>

                <!-- Last Name -->
                <div class="col-sm-6">
                    <div class="form-group">
                        <label>Last Name</label>
                        <input class="form-control" name="last_name" type="text" value="${patient.last_name}">
                    </div>
                </div>

                <!-- Date of Birth -->
                <div class="col-sm-6">
                    <div class="form-group">
                        <label>Date of Birth</label>
                        <input class="form-control" name="date_of_birth" type="date" value="${patient.date_of_birth}">
                    </div>
                </div>

                <!-- Gender -->
                <div class="col-sm-6">
                    <div class="form-group gender-select">
                        <label class="gen-label">Gender:</label>
                        <div class="form-check-inline">
                            <label class="form-check-label">
                                <input type="radio" name="gender" class="form-check-input" value="Male" ${patient.gender === 'Male' ? 'checked' : ''}> Male
                            </label>
                        </div>
                        <div class="form-check-inline">
                            <label class="form-check-label">
                                <input type="radio" name="gender" class="form-check-input" value="Female" ${patient.gender === 'Female' ? 'checked' : ''}> Female
                            </label>
                        </div>
                    </div>
                </div>

                <!-- Contact Number -->
                <div class="col-sm-6">
                    <div class="form-group">
                        <label>Contact Number</label>
                        <input class="form-control" name="contact_number" type="text" value="${patient.contact_number}">
                    </div>
                </div>

                <!-- Email -->
                <div class="col-sm-6">
                    <div class="form-group">
                        <label>Email</label>
                        <input class="form-control" name="email" type="email" value="${patient.email}">
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
        
        $('#patient-info-row').html(patientDataHtml);

        // Add form submission handler
        $('#patientForm').on('submit', function(e) {
            e.preventDefault(); // Prevent default form submission
            
            let patientId = localStorage.getItem('patientId');
            let formData = {
                first_name: $('input[name="first_name"]').val(),
                last_name: $('input[name="last_name"]').val(),
                date_of_birth: $('input[name="date_of_birth"]').val(),
                gender: $('input[name="gender"]:checked').val(),
                contact_number: $('input[name="contact_number"]').val(),
                email: $('input[name="email"]').val()
            };

            $.ajax({
                url: `/laboratory/get-patient/${patientId}/`, // Adjust the endpoint as needed
                type: 'PUT',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                },
                data: JSON.stringify(formData),
                success: function(response) {
                    var modal = createModal('Patient data updated successfully!');
                    modal.show();
                    
                    // Optionally refresh the data after update
                    fetchPatientData();
                },
                error: function(xhr, status, error) {
                    console.log("Error updating patient data:", error);
                    
                    var errorMessage = 'Failed to update patient data.';
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
    fetchPatientData();
});
