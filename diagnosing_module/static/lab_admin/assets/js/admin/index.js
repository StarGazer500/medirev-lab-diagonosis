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
    

    function formatDate(dateString) {
        if (!dateString) return 'N/A';
        
        const date = new Date(dateString);
        if (isNaN(date.getTime())) return dateString; // Return original if invalid
        
        const day = String(date.getDate()).padStart(2, '0');
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const year = String(date.getFullYear()).slice(-2);
        
        return `${day}-${month}-${year}`;
    }
    
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
        // let formattedOrderDate = formatDate(labrequest.order_date);
        let formattedRequestDate = formatDate(labrequest.requested_date);
        console.log(labrequest.request_status)
        
        // Create table row with lab request data
        var labrequestRow = `


          <tr data-labrequest-id="${labrequest.id}" >
            <td style="min-width: 200px;">
                <a class="avatar" href="{% url 'profile' %}">B</a>
                <h2><a href="{% url 'profile' %}"> ${labrequest.patient} <span>New York, USA</span></a></h2>
            </td>                 
            <td>
                <h5 class="time-title p-0">Appointment Status </h5>
               <p>${labrequest.request_status}</p>
            </td>
            <td>
                <h5 class="time-title p-0">Timing</h5>
                <p>${formattedRequestDate}</p>
            </td>
            <td class="text-right">
                <a href= "/laboratory/appointments/" class="btn btn-outline-primary take-btn">Take up</a>
                
            </td>
        </tr>


        `;

        $('#appointment-tbody').append(labrequestRow);

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

    fetchLabRequestData()


        // Function to fetch patient data from the server
        function fetchPatientData() {
            $.ajax({
                url: '/laboratory/get-all-patient/', // Replace with your actual endpoint
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


        function appendPatientToTable(patient) {
            
            
            // Create table row with patient data
            var patientRow = `


                <tr>
                    <td>
                        <img width="28" height="28" class="rounded-circle" src="{% static 'lab_admin/assets/img/user.jpg' %}" alt=""> 
                        <h2>${patient.first_name} ${patient.last_name}e</h2>
                    </td>
                    <td>${patient.email}</td>
                    <td>${patient.contact_number}</td>
                     <td class="text-right"><a href= "/laboratory/patients/" class="btn btn-outline-primary take-btn">Take up</a></td>
                </tr>
            `;
            
            // Append the row to the table body
            $('#patient-tbody').append(patientRow);
        }

        fetchPatientData()


        function fetchDoctorsData(doctor_id) {
            $.ajax({
                url: '/laboratory/get-all-doctor/', // Your endpoint to get all doctors
                type: 'GET',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken') // CSRF token for security
                },
                success: function(response) {
                    // Check if response contains doctor data
                    $('#doctors-list').empty();
                    // console.log(response)
                    
                    // Check if response has data
                    if (response && response.length > 0) {
                        console.log("res",response)
                        // console.log(response)
                        // Append each patient to the table
                        $.each(response, function(index, doctor) {
                            appendDoctorToTable(doctor);
                        });
                    } else {
                        // Show message if no patients
                        $('#doctors-list').append('<p>No doctor records found<p>');
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
    


        function appendDoctorToTable(doctor) {
            
            
            // Create table row with patient data
            var doctorList = `


               <li>
                <div class="contact-cont">
                    <div class="float-left user-img m-r-10">
                        <a href="/laboratory/profile/" title="John Doe"><img src="{% static 'lab_admin/assets/img/user.jpg' %}" alt="" class="w-40 rounded-circle"><span class="status online"></span></a>
                    </div>
                    <div class="contact-info">
                        <span class="contact-name text-ellipsis">${doctor.first_name} ${doctor.last_name}</span>
                        <span class="contact-date">${doctor.specialty}</span>
                    </div>
                </div>
             </li>
            `;
            
            // Append the list to doctor list
            $('#doctors-list').append(doctorList);
        }

    
        fetchDoctorsData()
})