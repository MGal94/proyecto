console.log(location.search); // Lee los argumentos pasados a este formulario
var id = location.search.substr(4);
console.log(id);

const { createApp } = Vue;

createApp({
    data() {
        return {
            id: 0,
            nombre: "",
            categoria: "",
            precio: "",
            stock: "",
            url: 'http://localhost:5000/productos/' + id,
        };
    },
    methods: {
        fetchData(url) {
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    this.id = data.id;
                    this.nombre = data.nombre;
                    this.categoria = data.categoria;
                    this.precio = data.precio;
                    this.stock = data.stock;
                })
                .catch(err => {
                    console.error(err);
                    this.error = true;
                });
        },
        modificar() {
            let producto = {
                nombre: this.nombre,
                categoria: this.categoria,
                precio: this.precio,
                stock: this.stock,
            };
            var options = {
                body: JSON.stringify(producto),
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                redirect: 'follow'
            };
            fetch(this.url, options)
                .then(function () {
                    alert("Registro modificado");
                    window.location.href = "./index.html";
                })
                .catch(err => {
                    console.error(err);
                    alert("Error al Modificar");
                });
        }
    },
    created() {
        this.fetchData(this.url);
    },
}).mount('#app');