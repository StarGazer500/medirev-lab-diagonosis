$(document).ready(function() {
    // Function to fetch lab request data from the server
    function fetchLabRequestData() {
        $.ajax({
            url: '/laboratory/get-all-laborder-request/',
            type: 'GET',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            success: function(response) {
                // Clear existing table rows
                $('#labrequest-tbody').empty();
                
                // Check if response has data
                if (response && response.length > 0) {
                    console.log("res", response);
                    
                    // Append each lab request to the table
                    $.each(response, function(index, labrequest) {
                        appendLabRequestToTable(labrequest);
                    });
                } else {
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
            <tr>
                <td>${labrequest.id}</td>
                <td>${labrequest.patient}</td>
                <td>${labrequest.test_description}</td>
                <td>${formattedOrderDate}</td>
                <td>${formattedRequestDate}</td>
                <td>${labrequest.request_status}</td>
                <td class="text-right">
                    <div class="dropdown dropdown-action">
                        <a href="#" class="action-icon dropdown-toggle" data-toggle="dropdown" aria-expanded="false"><i class="fa fa-ellipsis-v"></i></a>
                        <div class="dropdown-menu dropdown-menu-right">
                            <a class="dropdown-item" href="/laboratory/edit-labrequest/${labrequest.id}/"><i class="fa fa-pencil m-r-5"></i> Edit</a>
                            <a class="dropdown-item delete-labrequest-btn" href="#" data-labrequest-id="${labrequest.id}"><i class="fa fa-trash-o m-r-5"></i> Delete</a>
                        </div>
                    </div>
                </td>
            </tr>
        `;
        
        // Append the row to the table body
        $('#labrequest-tbody').append(labrequestRow);
    }
    
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
                url: `/laboratory/delete-labrequest/${id}/`,
                type: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                },
                success: function(response) {
                    modal.hide();
                    
                    // Show success message
                    var successModal = createModal("Lab Request record deleted successfully.");
                    successModal.show();
                    
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
    $(document).ready(function() {
        // Check if the datetimepicker function exists before calling it
        if ($.fn.datetimepicker) {
            $('.datetimepicker').datetimepicker({
                format: 'DD-MM-YYYY'
            });
        } else {
            console.log("Datetimepicker plugin not loaded. Make sure to include the plugin.");
        }
    });
    
    // Initial load of lab request data
    fetchLabRequestData();
});