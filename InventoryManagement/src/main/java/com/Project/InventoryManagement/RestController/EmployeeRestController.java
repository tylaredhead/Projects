package com.Project.InventoryManagement.RestController;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.Project.InventoryManagement.Entity.Stock;
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
    public ResponseEntity<List<Stock>> findByQuantity(int quantity){
        List<Stock> stock = inventoryService.findByQuantity(quantity);
        return (stock != null) ? ResponseEntity.ok(stock) : ResponseEntity.status(HttpStatus.NOT_FOUND).build();
    }
}
