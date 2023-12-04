const { createApp } = Vue;

createApp({
    data() {
        return {
            productos: [],
            url: 'http://127.0.0.1:5000/productos',
            error: false,
            cargando: true,
            id: 0,
            nombre: '',
            categoria: '',
            precio: '',
            stock: '',
        };
    },
    methods: {
        fetchData(url) {
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    this.productos = data;
                    this.cargando = false;
                })
                .catch(err => {
                    console.error(err);
                    this.error = true;
                });
        },
        eliminar(producto) {
            const url = this.url + '/' + producto;
            var options = {
                method: 'DELETE',
            };
            fetch(url, options)
                .then(response => response.json())
                .then(response => {
                    location.reload();
                })
        },
        grabar(){
            let producto = {
                nombre: this.nombre,
                categoria : this.categoria,
                precio: this.precio,
                stock : this.stock,
            };
            var options = {
                method: 'POST',
                body: JSON.stringify(producto),
                headers: { 'Content-Type': 'application/json' },
                redirect: 'follow'
            };
            fetch(this.url, options)
            .then(function () {
                alert('Se registro el nuevo producto');
                window.location.href = './index.html';
            })
            .catch(err => {
                console.error(err);
            });
        }
    },
    
    created() {
        this.fetchData(this.url)
    }


}).mount('#app');