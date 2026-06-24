async function toggleActive(id_user, current) {
    const newValue = current === 1 ? 0 : 1;

    const response = await fetch(`/api/v1/admin/users/${id_user}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ active: newValue }),
    });

    if (response.ok) {
        location.reload();
    } else {
        const data = await response.json();
        alert(data.message);
    }
}

async function toggleAdmin(id_user, current) {
    const newValue = current === 1 ? 0 : 1;

    const response = await fetch(`/api/v1/admin/users/${id_user}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ admin: newValue }),
    });

    if (response.ok) {
        location.reload();
    } else {
        const data = await response.json();
        alert(data.message);
    }
}
