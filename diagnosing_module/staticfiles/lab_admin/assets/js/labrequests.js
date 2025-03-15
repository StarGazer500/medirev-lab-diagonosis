$(document).ready(function() {
    // Function to fetch Medirev request data from the server
    function fetchMedirevRequestData() {
        $.ajax({
            url: '/Medirevoratory/get-all-Medirevorder-request/',
            type: 'GET',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            success: function(response) {
                // Clear existing table rows
                $('#Medirevrequest-tbody').empty();
                
                // Check if response has data
                if (response && response.length > 0) {
                    console.log("res", response);
                    
                    // Append each Medirev request to the table
                    $.each(response, function(index, Medirevrequest) {
                        appendMedirevRequestToTable(Medirevrequest);
                    });
                } else {
                    // Show message if no Medirev requests
                    $('#Medirevrequest-tbody').append('<tr><td colspan="7" class="text-center">No Medirev Request records found</td></tr>');
                }
            },
            error: function(xhr, status, error) {
                console.log("Error fetching Medirev Request data:", error);
                
                var errorMessage = 'Failed to load Medirev Request data.';
                if (xhr.responseJSON && xhr.responseJSON.message) {
                    errorMessage = xhr.responseJSON.message;
                }
                
                var modal = createModal(errorMessage);
                modal.show();
            }
        });
    }
    
    // Function to append a single Medirev request to the table
    function appendMedirevRequestToTable(Medirevrequest) {
        // Format dates (assuming date is in ISO format)
        let formattedOrderDate = formatDate(Medirevrequest.order_date);
        let formattedRequestDate = formatDate(Medirevrequest.requested_date);
        
        // Create table row with Medirev request data
        var MedirevrequestRow = `
            <tr>
                <td>${Medirevrequest.id}</td>
                <td>${Medirevrequest.patient}</td>
                <td>${Medirevrequest.test_description}</td>
                <td>${formattedOrderDate}</td>
                <td>${formattedRequestDate}</td>
                <td>${Medirevrequest.request_status}</td>
                <td class="text-right">
                    <div class="dropdown dropdown-action">
                        <a href="#" class="action-icon dropdown-toggle" data-toggle="dropdown" aria-expanded="false"><i class="fa fa-ellipsis-v"></i></a>
                        <div class="dropdown-menu dropdown-menu-right">
                            <a class="dropdown-item" href="/Medirevoratory/edit-Medirevrequest/${Medirevrequest.id}/"><i class="fa fa-pencil m-r-5"></i> Edit</a>
                            <a class="dropdown-item delete-Medirevrequest-btn" href="#" data-Medirevrequest-id="${Medirevrequest.id}"><i class="fa fa-trash-o m-r-5"></i> Delete</a>
                        </div>
                    </div>
                </td>
            </tr>
        `;
        
        // Append the row to the table body
        $('#Medirevrequest-tbody').append(MedirevrequestRow);
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
    
    // Delete Medirev request handler (using event delegation)
    $(document).on('click', '.delete-Medirevrequest-btn', function(e) {
        e.preventDefault();
        const MedirevrequestId = $(this).data('Medirevrequest-id');
        
        // Show confirmation modal
        var modal = createModal(`Are you sure you want to delete this Medirev Request record? <br><br>
            <div class="text-center">
                <button type="button" class="btn btn-danger" id="confirmDelete" data-id="${MedirevrequestId}">Delete</button>
                <button type="button" class="btn btn-secondary ms-2" data-bs-dismiss="modal">Cancel</button>
            </div>`);
        modal.show();
        
        // Handle confirm delete button
        $('#confirmDelete').click(function() {
            const id = $(this).data('id');
            
            $.ajax({
                url: `/Medirevoratory/delete-Medirevrequest/${id}/`,
                type: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                },
                success: function(response) {
                    modal.hide();
                    
                    // Show success message
                    var successModal = createModal("Medirev Request record deleted successfully.");
                    successModal.show();
                    
                    // Refresh Medirev request list
                    fetchMedirevRequestData();
                },
                error: function(xhr, status, error) {
                    console.log("Error deleting Medirev Request:", error);
                    
                    var errorMessage = 'Failed to delete Medirev Request record.';
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
    
    // Initial load of Medirev request data
    fetchMedirevRequestData();
});