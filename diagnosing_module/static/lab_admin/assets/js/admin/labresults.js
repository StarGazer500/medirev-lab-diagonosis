$(document).ready(function() {
    // Function to fetch lab request data from the server
    function fetchLabResultsData() {
        $.ajax({
            url: '/laboratory/get-all-lab-result/',
            type: 'GET',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            success: function(response) {
                // Clear existing table rows
                $('#labresult-tbody').empty();
                
                // Check if response has data
                if (response && response.length > 0) {
                    console.log("res", response);
                    
                    // Append each lab request to the table
                    $.each(response, function(index, labresult) {
                        appendLabResultsToTable(labresult);
                    });
                } else {
                    // Show message if no lab requests
                    $('#labresult-tbody').append('<tr><td colspan="7" class="text-center">No Lab Results records found</td></tr>');
                }
            },
            error: function(xhr, status, error) {
                console.log("Error fetching Lab Results data:", error);
                
                var errorMessage = 'Failed to load Lab Results data.';
                if (xhr.responseJSON && xhr.responseJSON.message) {
                    errorMessage = xhr.responseJSON.message;
                }
                
                var modal = createModal(errorMessage);
                modal.show();
            }
        });
    }
    
    // Function to append a single lab request to the table
    function  appendLabResultsToTable(labresult) {
        // Format dates (assuming date is in ISO format)
        let formattedTestDate = formatDate(labresult.test_date);
        let formattedCreatedAttDate = formatDate(labresult.created_at);
        
        // Create table row with lab request data
        var labresultRow = `
            <tr data-labresult-id="${labresult.id}">
                <td>${labresult.id}</td>
                <td>${labresult.result}</td>
                <td>${formattedTestDate}</td>
                <td>${formattedCreatedAttDate}</td>
                <td class="text-right">
                    <div class="dropdown dropdown-action">
                        <a href="#" class="action-icon dropdown-toggle" data-toggle="dropdown" aria-expanded="false"><i class="fa fa-ellipsis-v"></i></a>
                        <div class="dropdown-menu dropdown-menu-right">
                            <a class="dropdown-item edit-labresult-btn" href="/laboratory/edit-lab-result/"><i class="fa fa-pencil m-r-5"></i> Edit</a>
                            <a class="dropdown-item delete-labresult-btn" href="#" data-labresult-id="${labresult.id}"><i class="fa fa-trash-o m-r-5"></i> Delete</a>
                            <a class="dropdown-item add-lab-report-btn" href="/laboratory/add-lab-report/"><i class="fa fa-pencil m-r-5"></i> Generate Report</a> 
                        </div>
                    </div>
                </td>
            </tr>
        `;
        
        // Append the row to the table body
        $('#labresult-tbody').append(labresultRow);

    }

    $(document).on('click', '.add-lab-result-btn', function(event) {
        event.preventDefault(); // Prevent default action (navigation)
       
    
      
        localStorage.setItem("source_url",window.location.href)
        

        window.location.href = `/laboratory/add-lab-result/`;
    });


    $(document).on('click', '.edit-labresult-btn', function(event) {
        event.preventDefault(); // Prevent default action (navigation)
       
    
        // Get the parent row of the clicked Edit button
        var labresultRow = $(this).closest('tr');
        // console.log("patient email",patientRow)
        
        // Extract the email and other necessary information from the row
        // var patientEmail = patientRow.data('patient-email');
        // console.log(patientEmail)
        var labresultId =labresultRow.data('labresult-id');
        console.log("id",labresultId)
        
        // For now, log the email (you can store it in localStorage, sessionStorage, or use it directly)
        // console.log("Patient Email:", patientEmail);
        // console.log("Patient ID:", patientId);
    
        // Store the email in localStorage (or sessionStorage) if needed
        // localStorage.setItem('patientEmail', patientEmail);
        localStorage.setItem('labresultId', labresultId);

        // console.log("patient email",patientEmail)
    
    
        // Redirect to the Edit page or do something else
        window.location.href = `/laboratory/edit-lab-result/`;
    });


    $(document).on('click', '.add-lab-report-btn', function(event) {
        event.preventDefault(); // Prevent default action (navigation)
       
    
        // Get the parent row of the clicked Edit button
        var labresultRow = $(this).closest('tr');
        // console.log("patient email",patientRow)
        
        // Extract the email and other necessary information from the row
        // var patientEmail = patientRow.data('patient-email');
        // console.log(patientEmail)
        var labresultId =labresultRow.data('labresult-id');
      
        
        // For now, log the email (you can store it in localStorage, sessionStorage, or use it directly)
        // console.log("Patient Email:", patientEmail);
        // console.log("Patient ID:", patientId);
    
        // Store the email in localStorage (or sessionStorage) if needed
        // localStorage.setItem('patientEmail', patientEmail);
        localStorage.setItem('labresultId', labresultId);
        localStorage.setItem("source_url",window.location.href)
        

        // console.log("patient email",patientEmail)
    
    
        // Redirect to the Edit page or do something else
        window.location.href = `/laboratory/add-lab-report/`;
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
    
    // Delete lab request handler (using event delegation)
    $(document).on('click', '.delete-labresult-btn', function(e) {
        e.preventDefault();
        const labresultId = $(this).data('labresult-id');
        
        // Show confirmation modal
        var modal = createModal(`Are you sure you want to delete this Lab Result record? <br><br>
            <div class="text-center">
                <button type="button" class="btn btn-danger" id="confirmDelete" data-id="${labresultId}">Delete</button>
                <button type="button" class="btn btn-secondary ms-2" data-bs-dismiss="modal">Cancel</button>
            </div>`);
        modal.show();
        
        // Handle confirm delete button
        $('#confirmDelete').click(function() {
            const id = $(this).data('id');
            
            $.ajax({
                url: `/laboratory/get-lab-result/${id}/`,
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
                    var successModal = createModal("Lab Result record deleted successfully.");
                    successModal.show();

                    $('#dynamicModal').on('hidden.bs.modal', function() {
                        $('.modal-backdrop').remove();
                        $('body').removeClass('modal-open');
                        $('body').css('padding-right', '');
                        $(this).remove();
                    });
                        
                    
                    // Refresh lab request list
                    fetchLabResultsData();
                },
                error: function(xhr, status, error) {
                    console.log("Error deleting Lab Result:", error);
                    
                    var errorMessage = 'Failed to delete Lab Result record.';
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
    
    // Create modal function
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
    
    // Handle datetimepicker error
   
    
    // Initial load of lab request data
    fetchLabResultsData();
});