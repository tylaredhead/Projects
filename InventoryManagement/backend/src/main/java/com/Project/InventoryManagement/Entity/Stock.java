package com.Project.InventoryManagement.Entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;

@Entity
public class Stock {
    @Id
    @Column(name="productId", unique=true)
    private int id;
    @Column(name="rating")
    private String rating;
    @Column(name="quantity")
    private int quantity;
    
    public Stock(){}

    public Stock(int id, String rating, int quantity){
        this.id = id;
        this.rating = rating;
        this.quantity = quantity;
    }

    public int getId(){
        return id;
    }

    public void setId(int id){
        this.id = id;
    }

    public String getRating(){
        return rating;
    }

    public void setRating(String rating){
        this.rating = rating;
    }

    public int getQuantity(){
        return quantity;
    }

    public void setQuantity(int quantity){
        this.quantity = quantity;
    }

    @Override
    public String toString(){
        return "Stock{" + id + ", " + rating + ", " + quantity + "}";
    }
}   


