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

}
