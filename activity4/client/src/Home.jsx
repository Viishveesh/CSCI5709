import React from "react";
import banner from "./assets/Images/banner.png";

function Home(){
    return(
        <>
        <section id="banner">
            <div className="container banner-cnt">
                <div className="row">
                    <div className="col-md-6 col-12 col-sm-12 col-lg-6 banner-left">
                        <h1 className="banner-h1">
                            Welcome to ProdManager
                        </h1>
                        <p className="banner-p">
                            Effortlessly manage your products with our all-in-one tool. Create, view, edit and delete products - fast, simple and reliable.
                        </p>
                        <button className="btn btn-lg btn-light">
                            Explore Products
                        </button>
                    </div>
                    <div className="col-md-6 col-12 col-sm-12 col-lg-6">
                        <img src={banner} className="banner-img" />
                    </div>
                </div>
            </div>
            </section>
        </>
    )
}

export default Home;