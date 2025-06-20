import React, { useState, useEffect } from "react";
import axios from "axios";

const URL = "http://localhost:5000/products-info";

function Products() {

  const [error, setError] = useState("");
  
  const [products, setProducts] = useState([]);
  const [mode, setMode] = useState("none");
  const [searchTerm, setSearchTerm] = useState("");
  const [sortOption, setSortOption] = useState("");
  const [newProduct, setNewProduct] = useState({
    name: "",
    description: "",
    price: "",
  });

  useEffect(() => {
    setMode("list");
    getProducts();
  }, []);

  const getProducts = async () => {
  try {
    const token = localStorage.getItem("token");
    const res = await axios.get(URL, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    setProducts(res.data);
  } catch (error) {
    console.error("Error fetching products:", error);
  }
};

  const handleChange = (e) => {
    setNewProduct({ ...newProduct, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
  e.preventDefault();
  setError("");

  if (!newProduct.name || !newProduct.price) {
    setError("Name and Price are required.");
    return;
  }

  try {
    const token = localStorage.getItem("token");

    await axios.post(URL, {
      ...newProduct,
      price: parseFloat(newProduct.price),
    }, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    setNewProduct({ name: "", description: "", price: "" });
    setMode("list");
    getProducts();
  } catch (error) {
    if (error.response && error.response.data.error) {
      setError(error.response.data.error);
    } else {
      setError("Something went wrong. Please try again.");
    }
  }
};


  return (
    <div className="container text-center mt-5">
      <h2 className="mb-4">Product Overview</h2>

      <div className="d-flex justify-content-center gap-3 mb-4">
        {mode !== "add" && (
          <button className="btn btn-primary" onClick={() => setMode("add")}>
            Add Product
          </button>
        )}
        {mode !== "list" && (
          <button className="btn btn-primary" onClick={() => setMode("list")}>
            List Product
          </button>
        )}
        {mode !== "none" && (
          <button className="btn btn-secondary" onClick={() => setMode("none")}>
            Cancel
          </button>
        )}
      </div>

      {mode === "add" && (
        <div className="card mx-auto p-4" style={{ maxWidth: "400px" }}>
          <h5 className="mb-3 text-start">Add a New Product</h5>
          {error && <div className="alert alert-danger">{error}</div>}
          <form onSubmit={handleSubmit}>
            <div className="mb-3 text-start">
              <label className="form-label">Product Name</label>
              <input
                type="text"
                name="name"
                value={newProduct.name}
                onChange={handleChange}
                className="form-control"
                required
              />
            </div>
            <div className="mb-3 text-start">
              <label className="form-label">Description</label>
              <input
                type="text"
                name="description"
                value={newProduct.description}
                onChange={handleChange}
                className="form-control"
              />
            </div>
            <div className="mb-3 text-start">
              <label className="form-label">Price</label>
              <input
                type="number"
                name="price"
                value={newProduct.price}
                onChange={handleChange}
                className="form-control"
                required
              />
            </div>
            <button type="submit" className="btn btn-success">
              Submit
            </button>
          </form>
        </div>
      )}

      {mode === "list" && (
        <div className="mt-4 text-start">
          <h4>List Products</h4>
          <div className="d-flex justify-content-between mb-3">
        <input
          type="text"
          className="form-control w-50"
          placeholder="Search by name or description..."
          onChange={(e) => setSearchTerm(e.target.value.toLowerCase())}
        />

        <select
          className="form-select w-25"
          onChange={(e) => setSortOption(e.target.value)}
          defaultValue=""
        >
          <option value="" disabled>Sort By</option>
          <option value="price">Price</option>
          <option value="createdAt">Created At</option>
        </select>
      </div>
          <table className="table table-bordered mt-3">
            <thead className="table-light">
              <tr>
                <th>Name</th>
                <th>Description</th>
                <th>Price ($)</th>
              </tr>
            </thead>
            <tbody>
              {products.length > 0 ? (
      [...products]
    .filter((product) =>
      product.name.toLowerCase().includes(searchTerm) ||
      product.description.toLowerCase().includes(searchTerm)
    )
    .sort((a, b) => {
      if (sortOption === "price") {
        return parseFloat(a.price) - parseFloat(b.price);
      } else if (sortOption === "createdAt") {
        return new Date(a.createdAt) - new Date(b.createdAt);
      }
      return 0;
    })
    .map((product) => (
                  <tr key={product.name}>
                    <td>{product.name}</td>
                    <td>{product.description}</td>
                    <td>${parseFloat(product.price).toFixed(2)}</td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="4" className="text-center">
                    No products added yet.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default Products;