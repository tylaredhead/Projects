package com.Project.InventoryManagement.Entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;

@Entity
public class Product {
    @Id
    @GeneratedValue(strategy=GenerationType.AUTO)
    @Column(unique=true)
    private int productId;
    private String productName;
    private String productDesc;
    private String productType;
    private int supplierId;
    private float price;

    public Product(){}

    public Product(String productName, String productDesc, String productType, int supplierId, float price){
        this.productName = productName;
        this.productDesc = productDesc;
        this.productType = productType;
        this.supplierId = supplierId;
        this.price = price;
    }

    public int getProductId(){
        return productId;
    }

    public void setProductId(int id){
        this.productId = id;
    }

    public String getProductName(){
        return productName;
    }

    public void setProductName(String name){
        this.productName = name;
    }

    public String getProductDesc(){
        return productDesc;
    }

    public void setProductDesc(String desc){
        this.productDesc = desc;
    }

    public String getProductType(){
        return productType;
    }

    public void setProductType(String type){
        this.productType = type;
    }

    public int getSupplierId(){
        return supplierId;
    }

    public void setSupplierId(int supplierId){
        this.supplierId = supplierId;
    }

    public float getPrice(){
        return price;
    }

    public void setPrice(float price){
        this.price = price;
    }

    @Override
    public String toString(){
        return "Product{" + productId + ", " + productName + ", " + productDesc + ", " + productType + ", " + supplierId + ", " + price + "}";
    }
}
