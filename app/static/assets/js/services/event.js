async function getMyNextEvent() {
  try {
    const response = await fetch("/event/myNext");
    if (!response.ok) {
      throw new Error("Failed to fetch the next event.");
    }
    const eventData = await response.json();
    return eventData;
  } catch (error) {
    console.error("Error fetching the next event:", error);
    return null;
  }
}
