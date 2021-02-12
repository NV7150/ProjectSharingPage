import PlaceHolder from "../img/PlaceHolder.png";

const CAN_CREATE_EVERYONE = "everyone";

export default {
    statusIcons: {
        "open-chat" : {icon: "mdi-account-group", color: "#424242"},
        "announce" : {icon: "mdi-account-voice", color: "#424242"},
        "problems" : {icon: "mdi-account-question", color:"#424242"},
        "open" : {icon: "mdi-alert-circle", color: "#C62828"},
        "solved" : {icon: "mdi-alert-circle-check", color: "#43A047"}
    },
    defaultProject : {
        title: "Loading...",
        projectId: -1,
        bg_image: PlaceHolder,
        subtitle: "",
        likes: 0
    },
    failedProject : {
        title: "404 Not Found",
        projectId: -1,
        bg_image: PlaceHolder,
        subtitle: "Something went wrong...",
        likes: 0
    },
    memberTypes: {
        "Admin" : {prop: "admin_users", send: "MEMBERTYPE_ADMIN"},
        "Advanced Member": {prop: "announce_users", send: "MEMBERTYPE_ANNOUNCE"},
        "Member": {prop: "members", send: "MEMBERTYPE_MEMBER"},
    },
    canCreateEveryone: CAN_CREATE_EVERYONE,
    channels: [
        {
            id : 0,
            name: "OpenChat",
            status: "open-chat",
            send: "THREADTYPE_OPENCHAT",
            canWrite: CAN_CREATE_EVERYONE,
            canCreate: CAN_CREATE_EVERYONE
        },
        {
            id : 1,
            name: "Announce",
            status: "announce",
            send: "THREADTYPE_ANNOUNCE",
            canWrite: "Advanced Member",
            canCreate: "Advanced Member"
        },
        {
            id : 2,
            name: "Problems",
            status: "problems",
            send: "THREADTYPE_PROBLEMS",
            canWrite: CAN_CREATE_EVERYONE,
            canCreate: "Member"
        }
    ],
}