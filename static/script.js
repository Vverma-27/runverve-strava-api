// utility function to render heart rate data
const renderHeartData = (id, data) => {
    const heartRateCtx = document.getElementById(id).getContext("2d");
    new Chart(heartRateCtx, {
        type: "line",
        data: {
            labels: data.map((_, index) => index),
            datasets: [
                {
                    label: "Heart Rate (bpm)",
                    data,
                    borderColor: "#e63946",
                    backgroundColor: "rgba(230, 57, 70, 0.1)",
                    fill: true,
                    tension: 0.4,
                },
            ],
        },
        options: {
            responsive: true,
        },
    });
};

// Fetch activities data from the server
async function fetchData() {
    try {
        const response = await fetch("/get_activities");

        if (!response.ok) {
            throw new Error(`Error: ${response.status} ${response.statusText}`);
        }

        const data = await response.json();

        if (data.length === 0) {
            document.getElementById("activities").innerHTML =
                "<h3>No activities found</h3>";
            return;
        }

        // Display activities
        for (const activity of data) {
            const activityEl = document.createElement("div");
            activityEl.className = "activity";
            activityEl.innerHTML = `
                <h3 class="name">${activity.name}</h3>
                <h6 style="margin:0;margin-top:1vmin;">Type: ${activity.sport_type
                }</h6>
                <div class="activity-data">
                <div class="time-data">
                <h5>Time Data</h5>
                <p>
  Active Duration:
  <strong>
    ${Math.floor(activity.moving_time / 3600)} hour${Math.floor(activity.moving_time / 3600) !== 1 ? "s" : ""
                } 
    ${Math.round((activity.moving_time % 3600) / 60)} minute${Math.round((activity.moving_time % 3600) / 60) !== 1 ? "s" : ""
                }
    ${activity.moving_time % 60} second${activity.moving_time % 60 !== 1 ? "s" : ""
                }
  </strong>
</p>
<p>
  Total Duration:
  <strong>
    ${Math.floor(activity.elapsed_time / 3600)} hour${Math.floor(activity.elapsed_time / 3600) !== 1 ? "s" : ""
                } 
    ${Math.round((activity.elapsed_time % 3600) / 60)} minute${Math.round((activity.elapsed_time % 3600) / 60) !== 1 ? "s" : ""
                } 
    ${activity.elapsed_time % 60} second${activity.elapsed_time % 60 !== 1 ? "s" : ""
                }
  </strong>
</p></div>
                <div class="distance-data">
                <h5>Workout Data</h5>
                <p>Distance:<strong> ${(activity.distance / 1000).toFixed(
                    2
                )} km</strong></p>
                <p>Calories:<strong> ${(activity.kilojoules / 4).toFixed(
                    2
                )} kcal</strong></p>
                </div>
                <div class="distance-data">
                <h5>Speed Data</h5>
                <p>Avg. Speed:<strong> ${activity.average_speed
                } km/h</strong></p>
                <p>Top Speed:<strong> ${activity.max_speed} km/h</strong></p>
                </div>
                <div class="heart-data">
                <h5>Heartrate Data</h5>
                ${activity.has_heartrate
                    ? `<canvas id="heartrate-${activity.name}">Show Heartrate Stream</canvas>`
                    : "<p>No Heartrate Data</p>"
                }
                </div>
                </div>
            `;
            document.getElementById("activities").appendChild(activityEl);
            if (activity.has_heartrate) {
                // if the activity has heart rate data, fetch and render it
                const stream = await fetch(`/get_stream?activity_id=${activity.id}`);
                const streamData = await stream.json();
                const heartRateData = streamData.data;
                renderHeartData(`heartrate-${activity.name}`, heartRateData);
            }
        }
    } catch (error) {
        showToast(`Failed to fetch data: ${error.message}`);
    }
}

// Helper function to display a toast
function showToast(message) {
    const toast = document.createElement("div");
    toast.className = "toast";
    toast.textContent = message;

    // Append the toast to the body
    document.body.appendChild(toast);

    // Remove the toast after 3 seconds
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

const fetchUserData = async () => {
    try {
        const response = await fetch("/get_user");

        if (!response.ok) {
            throw new Error(`Error: ${response.status} ${response.statusText}`);
        }

        const data = await response.json();

        // Display user data
        document.getElementById("username").textContent = "@" + data.username;
        document.getElementById("user-name").textContent =
            data.firstname + " " + data.lastname;
        if (data.profile) document.getElementById("user-dp").src = data.profile;
    } catch (error) {
        showToast(`Failed to fetch user data: ${error.message}`);
    }
};

// Profile dropdown expansion
const profileCircle = document.getElementById("profile-circle");
const profileDropdown = document.getElementById("profile-dropdown");

profileCircle.addEventListener("click", () => {
    profileDropdown.classList.toggle("visible");
});

window.onload = () => {
    // Load data on page load
    fetchData();
    fetchUserData();
};
