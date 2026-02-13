const net = require("net");

function send(command) {
    return new Promise((resolve, reject) => {
        const client = new net.Socket();

        client.connect(6740, "127.0.0.1", () => {
            client.write(command + "\n");
        });

        client.on("data", (data) => {
            resolve(data.toString().trim());
            client.destroy(); // close after response
        });

        client.on("error", reject);
    });
}

module.exports = { send };
