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
    
    
    function fetchLabReportData() {
        // let id = 1; // Replace with the actual patient ID if need
        // ed
        
        let labreporttId= localStorage.getItem('labreporttId');
        $.ajax({
            url: `/laboratory/get-lab-reports/${labreporttId}`, // Replace with your actual endpoint
            type: 'GET',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            success: function(response) {
                // Check if response has data
                if (response) {
                    console.log("report response data",response)
                    // Call the function to populate the patient data
                    populateLabReportData(response);
                    fetchDoctorsData(response.doctor_id)
                } else {
                    // Show message if no patient data found
                    $('#labreport-info-row').html('<div class="col-12 text-center">No Lab Reports records found</div>');
                }
            },
            error: function(xhr, status, error) {
                console.log("Error fetching Lab Reports data:", error);
                
                var errorMessage = 'Failed to load Lab Reports data.';
                if (xhr.responseJSON && xhr.responseJSON.message) {
                    errorMessage = xhr.responseJSON.message;
                }
                
                var modal = createModal(errorMessage);
                modal.show();
            }
        });
    }


    function fetchDoctorsData(doctor_id) {
        $.ajax({
            url: '/laboratory/get-all-doctor/', // Your endpoint to get all doctors
            type: 'GET',
            headers: {
                'X-CSRFToken': getCookie('csrftoken') // CSRF token for security
            },
            success: function(response) {
                // Check if response contains doctor data
                if (response && response.length > 0) {
                    let $doctorDropdown = $('#doctorDropdown');
                    $doctorDropdown.empty();  // Clear existing options
    
                    // Add a default option
                    $doctorDropdown.append('<option value="">Select a doctor</option>');
    
                    // Loop through each doctor and add them to the dropdown
                    response.forEach(function(doctor) {
                        let option = `<option value="${doctor.id}" ${doctor.id === doctor_id ? 'selected' : ''}>${doctor.first_name} ${doctor.last_name}</option>`;
                        $doctorDropdown.append(option);
                    });
    
                    // Show the doctor dropdown container
                    $('#doctorDropdownContainer').show();
                } else {
                    // Handle case when no doctors are found
                    console.log("No doctors found");
                    $('#doctorDropdownContainer').hide();
                }
            },
            error: function(xhr, status, error) {
                console.log("Error fetching doctor data:", error);
                var errorMessage = 'Failed to load doctor data.';
                if (xhr.responseJSON && xhr.responseJSON.message) {
                    errorMessage = xhr.responseJSON.message;
                }
                var modal = createModal(errorMessage);
                modal.show();
            }
        });
    }

    // Function to populate patient data into the div
    function populateLabReportData(labreport) {
        const labreportDataHtml = `
            <div class="col-lg-8 offset-lg-2">
        <form id="labreportForm">
            <div class="row">
                <!-- Lab Result ID-->
                    <div class="col-sm-6">
                    <div class="form-group">
                        <label>Lab Result ID</label>
                        <input class="form-control" name="lab_result_id" type="text" value="${labreport.lab_result}">
                    </div>
                    </div>
                
                    <!-- Doctor -->
                        <!-- Dropdown for selecting a doctor (initially hidden) -->
                        <div class="form-group" id="doctorDropdownContainer" style="display: none;">
                            <label>Doctor</label>
                            <select class="form-control" name="doctor_id" id="doctorDropdown">
                                <option value="">Select a doctor</option>
                                <!-- Doctor options will be appended here dynamically -->
                            </select>
                        </div>

                        <!-- Report Data -->
                    <div class="col-sm-6">
                        <div class="form-group">
                            <label>Report Data</label>
                            <textarea class="form-control" id="message" name="report_data">${labreport.report_data}</textarea>
                        </div>
                    </div>

                        <!-- Shared with Doctor -->
                    <div class="col-sm-6">
                        <div class="form-group">
                            <label>Shared With Doctor</label>
                            <input class="form-control" name="shared_with_doctor" type="checkbox" ${labreport.shared_with_doctor ? 'checked' : ''}>
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
        
        $('#labreport-info-row').html(labreportDataHtml);

        // Add form submission handler
        $('#labreportForm').on('submit', function(e) {
            e.preventDefault(); // Prevent default form submission
            
            let labreporttId= localStorage.getItem('labreporttId');
            let formData = {
    
                report_data : $('textarea[name="report_data"]').val().trim(),
                shared_with_doctor: $('input[name="shared_with_doctor"]').prop('checked'),
                doctor_id: $('#doctorDropdown').val() 
                
            };

            $.ajax({
                url: `/laboratory/get-lab-reports/${labreporttId}/`, // Adjust the endpoint as needed
                type: 'PUT',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                },
                data: JSON.stringify(formData),
                success: function(response) {
                    var modal = createModal('Lab Report updated successfully!');
                    modal.show();
                    
                    // Optionally refresh the data after update
                    fetchLabReportData();
                },
                error: function(xhr, status, error) {
                    console.log("Error updating Lab Report data:", error);
                    
                    var errorMessage = 'Failed to update Lab Report data.';
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
    fetchLabReportData();
});
