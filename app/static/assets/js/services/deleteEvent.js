document.addEventListener("DOMContentLoaded", function () {
    const deleteEventButtons = document.querySelectorAll(".deleteEventButton");

    deleteEventButtons.forEach((button) => {
        button.addEventListener("click", function () {
            console.log(this.id);
            const eventId = this.id.split("-")[1];
            console.log(`Deleting event with ID: ${eventId}`);
            const response = fetch(`api/v1/event/${eventId}`, {
                method: "DELETE",
            });
            if (response.ok) {
                window.location.reload();
            } else {
                console.error("Failed to delete event");
            }
        });
    });
});
