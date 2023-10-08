$(document).ready(function() {
    // When the guests_count select changes
    $("#guests_count").change(function() {
        var numGuests = parseInt($(this).val());

        // Remove any existing guest input fields
        $("#guestsContainer").empty();

        // Generate input fields for guests 2 to numGuests
        for (var i = 2; i <= numGuests; i++) {
            var guestHtml = `
                <div class="col-xl-12">
                    <input type="text" placeholder="Guest ${i} Name" name="guest_name_${i}" required>
                </div>
                <div class="col-xl-12">
                    <input type="email" placeholder="Guest ${i} Email" name="guest_email_${i}" required>
                </div>
                <div class="col-xl-12">
                    <textarea placeholder="Guest ${i} Message" name="guest_message_${i}"></textarea>
                </div>
            `;
            $("#guestsContainer").append(guestHtml);
        }
    });
});