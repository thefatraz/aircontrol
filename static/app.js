
// Gui lenh dieu khien den Python Flask
async function sendCommand(command) {
    try {
        const response = await fetch("/command", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                command: command
            })
        });

        const result = await response.json();

        document.getElementById("message").innerText =
            result.message;

        await updateStatus();

    } catch (error) {
        document.getElementById("message").innerText =
            "Khong the ket noi den may chu Python!";
        console.error(error);
    }
}


// Gui lenh tu o nhap van ban
function submitCommand() {
    const input = document.getElementById("commandInput");
    const command = input.value.trim();

    if (command === "") {
        alert("Vui long nhap lenh!");
        return;
    }

    sendCommand(command);
    input.value = "";
}


// Cap nhat trang thai may lanh
async function updateStatus() {
    try {
        const response = await fetch("/status");
        const status = await response.json();

        document.getElementById("power").innerText =
            status.power ? "ĐANG BẬT" : "ĐANG TẮT";

        document.getElementById("temperature").innerText =
            status.temperature;

        const modes = {
            cool: "Làm lạnh",
            dry: "Hút ẩm",
            fan: "Quạt"
        };

        const fans = {
            auto: "Tự động",
            high: "Mạnh",
            low: "Nhẹ"
        };

        document.getElementById("mode").innerText =
            modes[status.mode] || status.mode;

        document.getElementById("fan").innerText =
            fans[status.fan_speed] || status.fan_speed;

    } catch (error) {
        console.error("Loi cap nhat trang thai:", error);
    }
}


// Tu dong cap nhat moi 2 giay
updateStatus();
setInterval(updateStatus, 2000);
