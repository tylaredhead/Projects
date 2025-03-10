package com.Project.InventoryManagement.RestController;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.Project.InventoryManagement.Entity.Product;
import com.Project.InventoryManagement.Entity.Stock;
import com.Project.InventoryManagement.Service.InventoryService;

@RestController
@RequestMapping("/user")
public class UserRestController {
    private final InventoryService inventoryService;

    @Autowired
    public UserRestController(InventoryService inventoryService){
        this.inventoryService = inventoryService;
    }

    /*@PostMapping
    public ResponseEntity<Stock> createStock(@RequestBody Stock stock){
        Stock savedStock = inventoryService.saveStock(stock);
        // HTTP 201 - created
        return ResponseEntity.status(HttpStatus.CREATED).body(savedStock);
    }*/

    @GetMapping("/{id}")
    public ResponseEntity<Stock> findByStockId(@PathVariable int id){
        Stock stock = inventoryService.findById(id);
        return (stock != null) ? ResponseEntity.ok(stock) : ResponseEntity.status(HttpStatus.NOT_FOUND).build();
    }

    @GetMapping("/{productName}")
    public ResponseEntity<List<Stock>> findStockByProductName(@PathVariable String name){
        List<Stock> stock = inventoryService.findStockByProductName(name);
        return (stock != null) ? ResponseEntity.ok(stock) : ResponseEntity.status(HttpStatus.NOT_FOUND).build();
    }
    
    @GetMapping("/{rating}")
    public ResponseEntity<List<Stock>> findByRating(@PathVariable String rating){
        List<Stock> stock = inventoryService.findByRating(rating);
        return (stock != null) ? ResponseEntity.ok(stock) : ResponseEntity.status(HttpStatus.NOT_FOUND).build();
    }

    @PutMapping("/{id}")
    public ResponseEntity<Stock> updateQuantity(@PathVariable int id, @PathVariable int quantity){
        Stock stock = inventoryService.updateQuantity(id, quantity);
        return (stock != null) ? ResponseEntity.ok(stock) : ResponseEntity.status(HttpStatus.NOT_FOUND).build();
    }

    @GetMapping("/{productName}")
    public ResponseEntity<List<Product>> findByProductName(String name){
        List<Product> product = inventoryService.findByProductName(name);
        return (product != null) ? ResponseEntity.ok(product) : ResponseEntity.status(HttpStatus.NOT_FOUND).build();
    }

    @GetMapping("/{productDesc}")
    public ResponseEntity<List<Product>> findByProductDesc(String desc){
        List<Product> product = inventoryService.findByProductDesc(desc);
        return (product != null) ? ResponseEntity.ok(product) : ResponseEntity.status(HttpStatus.NOT_FOUND).build();
    }

    @GetMapping("/{productType}")
    public ResponseEntity<List<Product>> findByProductType(String type){
        List<Product> product = inventoryService.findByProductType(type);
        return (product != null) ? ResponseEntity.ok(product) : ResponseEntity.status(HttpStatus.NOT_FOUND).build();
    }

    @GetMapping("/{price}")
    public ResponseEntity<List<Product>> findByPrice(float price){
        List<Product> product = inventoryService.findByPrice(price);
        return (product != null) ? ResponseEntity.ok(product) : ResponseEntity.status(HttpStatus.NOT_FOUND).build();
    }
}
