import PlaceHolder from "../img/PlaceHolder.png";

export default {
    statusIcons: {
        "open-chat" : {icon: "mdi-account-group", color: "#424242"},
        "announce" : {icon: "mdi-account-voice", color: "#424242"},
        "problems" : {icon: "mdi-account-question", color:"#424242"},
        "open" : {icon: "mdi-alert-circle", color: "#C62828"},
        "solved" : {icon: "mdi-alert-circle-check", color: "#43A047"}
    },
    channels: [
        {name: "OpenChat", status: "open-chat"},
        {name: "Announce", status: "announce"},
        {name: "Problems", status: "problems"}
    ],
    defaultProject : {
        title: "Loading...",
        projectId: -1,
        bg_image: PlaceHolder,
        subtitle: ""
    },
    failedProject : {
        title: "404 Not Found",
        projectId: -1,
        bg_image: PlaceHolder,
        subtitle: "Something went wrong..."
    }
}