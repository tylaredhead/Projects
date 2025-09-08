package com.Project.InventoryManagement.DTO;

public class ProductDTO {
    private int id;
    private String name;
    private String description;
    private String type;
    private int quantity;
    private float price;
    private String rating;

    public ProductDTO(int id,
                      String name,
                      String description,
                      String type,
                      int quantity,
                      float price,
                      String rating) {
        this.id = id;
        this.name = name;
        this.description = description;
        this.type = type;
        this.quantity = quantity;
        this.price = price;
        this.rating = rating;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public int getQuantity() {
        return quantity;
    }

    public void setQuantity(int quantity) {
        this.quantity = quantity;
    }

    public float getPrice() {
        return price;
    }

    public void setPrice(float price) {
        this.price = price;
    }

    public String getRating() {
        return rating;
    }

    public void setRating(String rating) {
        this.rating = rating;
    }

    

}
