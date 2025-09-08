package com.Project.InventoryManagement.RestController;

import java.util.List;
import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
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

    @GetMapping("/stock/all")
    public ResponseEntity<List<Stock>> getAllStock(){
        List<Stock> stock = inventoryService.getAllStock();
        return (stock != null) ? ResponseEntity.ok(stock) : ResponseEntity.status(HttpStatus.NO_CONTENT).build();
    }

    @PostMapping("/supplier/all")
    public ResponseEntity<List<Supplier>> getAllSuppliers(){
        List<Supplier> allStock = inventoryService.getAllSuppliers();
        return (allStock != null) ? ResponseEntity.ok(allStock) : ResponseEntity.status(HttpStatus.NOT_FOUND).build();
    }

    @PostMapping("/supplier/get")
    public ResponseEntity<List<Supplier>> findSupplierInfo(@RequestBody Map<String, String> map){
        String name = map.get("name");
        int id;
        try { 
            id = Integer.parseInt(map.get("id"));
        } catch (Exception e) {
            id = -1;
        }

        if (id != -1) {
            List<Supplier> supplier = inventoryService.findBySupplierId(id);
            return (supplier != null) ? ResponseEntity.ok(supplier) : ResponseEntity.status(HttpStatus.NOT_FOUND).build();
        } else if (name != "") {
            List<Supplier> supplier = inventoryService.findBySupplierName(name);
            return (supplier != null) ? ResponseEntity.ok(supplier) : ResponseEntity.status(HttpStatus.NOT_FOUND).build();
        } else return ResponseEntity.status(HttpStatus.NOT_FOUND).build();
    }
}
