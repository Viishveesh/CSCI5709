import React from "react";


function ProductCard({ name, description, price, imageUrl })  {
  return (
    <div className="card h-100">
      <img src={imageUrl} className="card-img-top" alt={name} />
      <div className="card-body d-flex flex-column justify-content-between">
        <div>
          <h5 className="card-title">{name}</h5>
          <p className="card-text">{description}</p>
        </div>
        <div>
          <p className="fw-bold">${price}</p>
          <div className="d-flex gap-3">
            <span
              role="button"
              title="Edit"
              style={{ cursor: "pointer", color: "green" }}
            >
              <i className="fa fa-pencil" aria-hidden="true"></i>
            </span>
            <span
              role="button"
              title="Delete"
              style={{ cursor: "pointer", color: "red" }}
            >
              <i className="fa fa-trash-o" aria-hidden="true"></i>
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProductCard;