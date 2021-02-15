export default {
    name: "ErrorResolver",
    resolveError(router){
        router.push({
            name:'Error',
        });
    }
}