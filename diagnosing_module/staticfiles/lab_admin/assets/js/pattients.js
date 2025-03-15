$(document).ready(function() {
    // Function to fetch patient data from the server
    function fetchPatientData() {
        $.ajax({
            url: '/Medirevoratory/get-all-patient/', // Replace with your actual endpoint
            type: 'GET',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            success: function(response) {
                // Clear existing table rows
                $('#patient-tbody').empty();
                // console.log(response)
                
                // Check if response has data
                if (response && response.length > 0) {
                    console.log("res",response)
                    // console.log(response)
                    // Append each patient to the table
                    $.each(response, function(index, patient) {
                        appendPatientToTable(patient);
                    });
                } else {
                    // Show message if no patients
                    $('#patient-tbody').append('<tr><td colspan="8" class="text-center">No patient records found</td></tr>');
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
    
    // Function to append a single patient to the table
    function appendPatientToTable(patient) {
        // Format date (assuming date is in ISO format)
        let formattedDate = formatDate(patient.date_of_birth);
        
        // Create table row with patient data
        var patientRow = `
            <tr  data-patient-id="${patient.id}" >
               
                <td>${patient.first_name}</td>
                <td>${patient.last_name}</td>
                <td>${formattedDate}</td>
                <td>${patient.gender}</td>
                <td>${patient.contact_number}</td>
                <td>${patient.email}</td>
                <td class="text-right">
                    <div class="dropdown dropdown-action">
                        <a href="#" class="action-icon dropdown-toggle" data-toggle="dropdown" aria-expanded="false"><i class="fa fa-ellipsis-v"></i></a>
                        <div class="dropdown-menu dropdown-menu-right">
                            <a class="dropdown-item edit-patient-btn" href="/Medirevoratory/edit-patient/"><i class="fa fa-pencil m-r-5"></i> Edit</a>
                            <a class="dropdown-item delete-patient-btn" href="#" data-patient-id="${patient.id}" class="delete-patient-btn"><i class="fa fa-trash-o m-r-5"></i> Delete</a>
                        </div>
                    </div>
                </td>
            </tr>
        `;
        
        // Append the row to the table body
        $('#patient-tbody').append(patientRow);
    }

    $(document).on('click', '.edit-patient-btn', function(event) {
        event.preventDefault(); // Prevent default action (navigation)
       
    
        // Get the parent row of the clicked Edit button
        var patientRow = $(this).closest('tr');
        // console.log("patient email",patientRow)
        
        // Extract the email and other necessary information from the row
        // var patientEmail = patientRow.data('patient-email');
        // console.log(patientEmail)
        var patientId = patientRow.data('patient-id');
        console.log("id",patientId)
        
        // For now, log the email (you can store it in localStorage, sessionStorage, or use it directly)
        // console.log("Patient Email:", patientEmail);
        // console.log("Patient ID:", patientId);
    
        // Store the email in localStorage (or sessionStorage) if needed
        // localStorage.setItem('patientEmail', patientEmail);
        localStorage.setItem('patientId', patientId);

        // console.log("patient email",patientEmail)
    
    
        // Redirect to the Edit page or do something else
        window.location.href = `/Medirevoratory/edit-patient/`;
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
    
    // Get CSRF token from cookie (reusing your existing function)
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
    
    // Delete patient handler (using event delegation)
    $(document).on('click', '.delete-patient-btn', function(e) {
        e.preventDefault();
        const patientId = $(this).data('patient-id');
        
        // Show confirmation modal
        var modal = createModal(`Are you sure you want to delete this patient record? <br><br>
            <div class="text-center">
                <button type="button" class="btn btn-danger" id="confirmDelete" data-id="${patientId}">Delete</button>
                <button type="button" class="btn btn-secondary ms-2" data-bs-dismiss="modal">Cancel</button>
            </div>`);
        modal.show();
        
        // Handle confirm delete button
        $('#confirmDelete').click(function() {
            const id = $(this).data('id');
            
            $.ajax({
                url: `/Medirevoratory/delete-patient/${id}/`,
                type: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                },
                success: function(response) {
                    modal.hide();
                    
                    // Show success message
                    var successModal = createModal("Patient record deleted successfully.");
                    successModal.show();
                    
                    // Refresh patient list
                    fetchPatientData();
                },
                error: function(xhr, status, error) {
                    console.log("Error deleting patient:", error);
                    
                    var errorMessage = 'Failed to delete patient record.';
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
    

    $(document).on('click', '.delete-patient-btn', function(e) {
        e.preventDefault();
        const patientId = $(this).data('patient-id');
        
        // Show confirmation modal
        var modal = createModal(`Are you sure you want to delete this patient record? <br><br>
            <div class="text-center">
                <button type="button" class="btn btn-danger" id="confirmDelete" data-id="${patientId}">Delete</button>
                <button type="button" class="btn btn-secondary ms-2" data-bs-dismiss="modal">Cancel</button>
            </div>`);
        modal.show();
        
        // Handle confirm delete button
        $('#confirmDelete').click(function() {
            const id = $(this).data('id');
            
            $.ajax({
                url: `/Medirevoratory/delete-patient/${id}/`,
                type: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                },
                success: function(response) {
                    modal.hide();
                    
                    // Show success message
                    var successModal = createModal("Patient record deleted successfully.");
                    successModal.show();
                    
                    // Refresh patient list
                    fetchPatientData();
                },
                error: function(xhr, status, error) {
                    console.log("Error deleting patient:", error);
                    
                    var errorMessage = 'Failed to delete patient record.';
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
    // Initial load of patient data
    fetchPatientData();
    
    // Optional: Refresh data periodically (every 60 seconds)
    // setInterval(fetchPatientData, 60000);
    
    // Reuse your existing createModal function
    function createModal(bodyContent) {
        // Remove any existing modal with the same ID first
        $('#dynamicModal').remove();
        
        // Modal HTML structure with dynamic body content - Updated for Bootstrap 5
        var modalHTML = `
          <div class="modal fade" id="dynamicModal" tabindex="-1" aria-Medirevelledby="dynamicModalMedirevel" aria-hidden="true">
            <div class="modal-dialog">
              <div class="modal-content">
                <div class="modal-header">
                  <h5 class="modal-title" id="dynamicModalMedirevel">Notification</h5>
                  <button type="button" class="btn-close" data-bs-dismiss="modal" aria-Medirevel="Close"></button>
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
});