package com.Project.InventoryManagement.RestController;

import java.util.List;
import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.Project.InventoryManagement.DTO.ProductDTO;
import com.Project.InventoryManagement.Entity.Product;
import com.Project.InventoryManagement.Entity.Stock;
import com.Project.InventoryManagement.Service.InventoryService;

@RestController
@RequestMapping("/user")
public class UserRestController {
    protected final InventoryService inventoryService;

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
    /*
    @GetMapping("stock/id")
    public ResponseEntity<Stock> findByStockId(@PathVariable int id){
        Stock stock = inventoryService.findById(id);
        return (stock != null) ? ResponseEntity.ok(stock) : ResponseEntity.status(HttpStatus.NOT_FOUND).build();
    }

    @GetMapping("/stock/name")
    public ResponseEntity<List<Stock>> findStockByProductName(@PathVariable String name){
        List<Stock> stock = inventoryService.findStockByProductName(name);
        return (stock != null) ? ResponseEntity.ok(stock) : ResponseEntity.status(HttpStatus.NOT_FOUND).build();
    }
    
    @GetMapping("/stock/rating")
    public ResponseEntity<List<Stock>> findByRating(@PathVariable String rating){
        List<Stock> stock = inventoryService.findByRating(rating);
        return (stock != null) ? ResponseEntity.ok(stock) : ResponseEntity.status(HttpStatus.NOT_FOUND).build();
    }
    

    @PutMapping("/stock/quantity")
    public ResponseEntity<Stock> updateQuantity(@PathVariable int id, @PathVariable int quantity){
        Stock stock = inventoryService.updateQuantity(id, quantity);
        return (stock != null) ? ResponseEntity.ok(stock) : ResponseEntity.status(HttpStatus.NOT_FOUND).build();
    }

    @GetMapping("/product/name")
    public ResponseEntity<List<Product>> findByProductName(@PathVariable String name){
        List<Product> product = inventoryService.findByProductName(name);
        return (product != null) ? ResponseEntity.ok(product) : ResponseEntity.status(HttpStatus.NOT_FOUND).build();
    }

    @GetMapping("/product/desc")
    public ResponseEntity<List<Product>> findByProductDesc(@PathVariable String desc){
        List<Product> product = inventoryService.findByProductDesc(desc);
        return (product != null) ? ResponseEntity.ok(product) : ResponseEntity.status(HttpStatus.NOT_FOUND).build();
    }

    @GetMapping("/product/type")
    public ResponseEntity<List<Product>> findByProductType(@PathVariable String type){
        List<Product> product = inventoryService.findByProductType(type);
        return (product != null) ? ResponseEntity.ok(product) : ResponseEntity.status(HttpStatus.NOT_FOUND).build();
    }

    @GetMapping("/product/price")
    public ResponseEntity<List<Product>> findByPrice(@PathVariable float price){
        List<Product> product = inventoryService.findByPrice(price);
        return (product != null) ? ResponseEntity.ok(product) : ResponseEntity.status(HttpStatus.NOT_FOUND).build();
    }
    */

    @GetMapping("/product/info")
    public ResponseEntity<List<ProductDTO>> getProductInfo(@RequestBody Map<String, String> map){
        String name = map.get("name");
        String type = map.get("type");
        int id = (map.get("id") != null) ? Integer.parseInt(map.get("id")) : -1;
    
        if (id != -1) {
            ProductDTO obj = inventoryService.getProductStockById(id);
            return (obj != null) ? ResponseEntity.ok(List.of(obj)) : ResponseEntity.status(HttpStatus.NOT_FOUND).build();
        } else if (name != null && type != null) {
            List<ProductDTO> list = inventoryService.getProductsStockByNameAndType(name, type);
            return (list != null && !list.isEmpty()) ? ResponseEntity.ok(list) : ResponseEntity.status(HttpStatus.NOT_FOUND).build();
        } else if (name != null) {
            List<ProductDTO> list = inventoryService.getProductsStockByName(name);
            return (list != null && !list.isEmpty()) ? ResponseEntity.ok(list) : ResponseEntity.status(HttpStatus.NOT_FOUND).build();
        } else if (type != null) {
            List<ProductDTO> list = inventoryService.getProductsStockByType(type);
            return (list != null && !list.isEmpty()) ? ResponseEntity.ok(list) : ResponseEntity.status(HttpStatus.NOT_FOUND).build();
        } else return ResponseEntity.status(HttpStatus.NOT_FOUND).build();
    }
}
