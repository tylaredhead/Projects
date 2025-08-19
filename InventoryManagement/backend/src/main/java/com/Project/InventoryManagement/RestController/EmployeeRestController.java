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
import com.Project.InventoryManagement.Entity.Supplier;
import com.Project.InventoryManagement.Service.InventoryService;

@RestController
@RequestMapping("/employee")
public class EmployeeRestController extends UserRestController{
    @Autowired
    public EmployeeRestController(InventoryService inventoryService){
        super(inventoryService);
    }

    @GetMapping
    public ResponseEntity<List<Stock>> getAllStock(){
        List<Stock> stock = inventoryService.getAllStock();
        return (stock != null) ? ResponseEntity.ok(stock) : ResponseEntity.status(HttpStatus.NO_CONTENT).build();
    }

    @GetMapping("/{quantity}")
    public ResponseEntity<List<Stock>> findByQuantity(@PathVariable int quantity){
        List<Stock> stock = inventoryService.findByQuantity(quantity);
        return (stock != null) ? ResponseEntity.ok(stock) : ResponseEntity.status(HttpStatus.NOT_FOUND).build();
    }

    @PutMapping("/{rating}")
    public ResponseEntity<Stock> updateRating(@PathVariable int id, @PathVariable String rating){
        Stock stock = inventoryService.updateRating(id, rating);
        return (stock != null) ? ResponseEntity.ok(stock) : ResponseEntity.status(HttpStatus.NOT_FOUND).build();
    }

    @GetMapping
    public ResponseEntity<List<Supplier>> getAllSuppliers(){
        List<Supplier> allStock = inventoryService.getAllSuppliers();
        return (allStock != null) ? ResponseEntity.ok(allStock) : ResponseEntity.status(HttpStatus.NOT_FOUND).build();
    }

    @GetMapping("/{id}")
    public ResponseEntity<Supplier> findBySupplierId(@PathVariable int id){
        Supplier supplier = inventoryService.findBySupplierId(id);
        return (supplier != null) ? ResponseEntity.ok(supplier) : ResponseEntity.status(HttpStatus.NOT_FOUND).build();
    }

    @GetMapping("/{name}")
    public ResponseEntity<List<Supplier>> findBySupplierName(@PathVariable String name){
        List<Supplier> suppliers = inventoryService.findBySupplierName(name);
        return (suppliers != null) ? ResponseEntity.ok(suppliers) : ResponseEntity.status(HttpStatus.NOT_FOUND).build();
    }

    @GetMapping("/{supplierNo}")
    public ResponseEntity<List<Supplier>> findBySupplierNo(@PathVariable String no){
        List<Supplier> suppliers = inventoryService.findBySupplierNo(no);
        return (suppliers != null) ? ResponseEntity.ok(suppliers) : ResponseEntity.status(HttpStatus.NOT_FOUND).build();
    }

    @GetMapping("/{supplierEmail}")
    public ResponseEntity<List<Supplier>> findBySupplierEmail(@PathVariable String email){
        List<Supplier> suppliers = inventoryService.findBySupplierEmail(email);
        return (suppliers != null) ? ResponseEntity.ok(suppliers) : ResponseEntity.status(HttpStatus.NOT_FOUND).build();
    }

    @GetMapping
    public ResponseEntity<List<Product>> getAllProducts(){
        List<Product> products = inventoryService.getAllProducts();
        return (products != null) ? ResponseEntity.ok(products) : ResponseEntity.status(HttpStatus.NOT_FOUND).build();
    }

    @GetMapping("/{id}")
    public ResponseEntity<Product> findByProductId(@PathVariable int id){
        Product product = inventoryService.findByProductId(id);
        return (product != null) ? ResponseEntity.ok(product) : ResponseEntity.status(HttpStatus.NOT_FOUND).build();
    }

    @GetMapping("/{name}")
    public ResponseEntity<List<Product>> findProductBySupplierName(@PathVariable String name){
        List<Product> products = inventoryService.findProductBySupplierName(name);
        return (products != null) ? ResponseEntity.ok(products) : ResponseEntity.status(HttpStatus.NOT_FOUND).build();
    }
}
