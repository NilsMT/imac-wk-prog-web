document.addEventListener("DOMContentLoaded", function () {
    const deleteEventButtons = document.querySelectorAll(".deleteEventButton");

    deleteEventButtons.forEach((button) => {
        button.addEventListener("click", async function () {
            const eventId = this.id.split("-")[1];
            const response = await fetch(`/api/v1/events/${eventId}`, {
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
