document.addEventListener("DOMContentLoaded", function () {
    const toggleActiveButtons = document.querySelectorAll(
        ".toggleActiveButton",
    );

    toggleActiveButtons.forEach((button) => {
        button.addEventListener("click", async function () {
            const parts = this.id.split("-");
            const userId = parts.slice(1, -1).join("-");
            const admin = parts[parts.length - 1];
            console.log(
                `Toggling active for user ID: ${userId}, current state: ${active}`,
            );
            const response = await fetch(`/api/v1/admin/users/${userId}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ active: active === "1" ? 0 : 1 }),
            });
            if (response.ok) {
                window.location.reload();
            } else {
                console.error("Failed to toggle user active state");
            }
        });
    });

    const toggleAdminButtons = document.querySelectorAll(".toggleAdminButton");

    toggleAdminButtons.forEach((button) => {
        button.addEventListener("click", async function () {
            const parts = this.id.split("-");
            const userId = parts.slice(1, -1).join("-");
            const admin = parts[parts.length - 1];
            console.log(
                `Toggling admin for user ID: ${userId}, current state: ${admin}`,
            );
            const response = await fetch(`/api/v1/admin/users/${userId}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ admin: admin === "1" ? 0 : 1 }),
            });
            if (response.ok) {
                window.location.reload();
            } else {
                console.error("Failed to toggle user admin state");
            }
        });
    });
});
