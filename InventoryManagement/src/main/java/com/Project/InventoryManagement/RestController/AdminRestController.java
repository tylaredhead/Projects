package com.Project.InventoryManagement.RestController;


import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.Project.InventoryManagement.Entity.Stock;
import com.Project.InventoryManagement.Entity.Supplier;
import com.Project.InventoryManagement.Service.InventoryService;

@RestController
@RequestMapping("/admin")
public class AdminRestController extends EmployeeRestController{
    @Autowired
    public AdminRestController(InventoryService inventoryService){
        super(inventoryService);
    }

    @PostMapping
    public ResponseEntity<Stock> saveStock(@RequestBody Stock stock){
        stock = inventoryService.saveStock(stock);
        return ResponseEntity.ok(stock); 
    }

    @DeleteMapping("/{id}")
    public void deleteById(@PathVariable int id){
        inventoryService.deleteById(id);
    }

    @PostMapping
    public ResponseEntity<Supplier> saveSupplier(@RequestBody Supplier supplier){
        supplier = inventoryService.saveSupplier(supplier);
        return ResponseEntity.ok(supplier);
    }

    @PostMapping("/{name}")
    public ResponseEntity<Supplier> updateSupplierName(@PathVariable int id, @PathVariable String name){
        Supplier supplier = inventoryService.updateSupplierName(id, name);
        return (supplier != null) ? ResponseEntity.ok(supplier) : ResponseEntity.status(HttpStatus.NOT_FOUND).build();
    }

    @PostMapping("/{no}")
    public ResponseEntity<Supplier> updateSupplierNo(@PathVariable int id, @PathVariable String no){
        Supplier supplier = inventoryService.updateSupplierNo(id, no);
        return (supplier != null) ? ResponseEntity.ok(supplier) : ResponseEntity.status(HttpStatus.NOT_FOUND).build();
    }

    @PostMapping("/{email}")
    public ResponseEntity<Supplier> updateSupplierEmail(@PathVariable int id, @PathVariable String email){
        Supplier supplier = inventoryService.updateSupplierEmail(id, email);
        return (supplier != null) ? ResponseEntity.ok(supplier) : ResponseEntity.status(HttpStatus.NOT_FOUND).build();
    }

    @DeleteMapping("/{id}")
    public void deleteBySupplierId(@PathVariable int id){
        inventoryService.deleteBySupplierId(id);
    }

    @DeleteMapping("/{name}")
    public void deleteBySupplierName(@PathVariable String name){
        inventoryService.deleteBySupplierName(name);
    }
}
