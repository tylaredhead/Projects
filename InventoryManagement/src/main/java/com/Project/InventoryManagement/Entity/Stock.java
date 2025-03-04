package com.Project.InventoryManagement.Entity;

import jakarta.persistence.CascadeType;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.OneToOne;

@Entity
public class Stock {
    @Id
    private int id;
    private String rating;
    private int quantity;
    @OneToOne(cascade=CascadeType.ALL)
    @JoinColumn(name="id")
    private Product product;
    
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


