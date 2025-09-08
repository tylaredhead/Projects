package com.Project.InventoryManagement.RestController;

import java.util.List;
import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.Project.InventoryManagement.DTO.ProductDTO;
import com.Project.InventoryManagement.Service.InventoryService;

@RestController
@RequestMapping("/user")
public class UserRestController {
    protected final InventoryService inventoryService;

    @Autowired
    public UserRestController(InventoryService inventoryService){
        this.inventoryService = inventoryService;
    }

    @PostMapping("/product/get")
    public ResponseEntity<List<ProductDTO>> getProductInfo(@RequestBody Map<String, String> map){
        String name = map.get("name");
        String type = map.get("type");
        int id;
        try {
            id = Integer.parseInt(map.get("id"));
        } catch (Exception e) {
            id = -1;
        }

        List<ProductDTO> list = null;
        if (id != -1) list = inventoryService.getProductStockById(id);
        else if (name != "" && type != "") list = inventoryService.getProductsStockByNameAndType(name, type);
        else if (name != "") list = inventoryService.getProductsStockByName(name);
        else if (type != "") list = inventoryService.getProductsStockByType(type);
        else {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).build();
        }
        return (list != null && !list.isEmpty()) ? ResponseEntity.ok(list) : ResponseEntity.status(HttpStatus.NOT_FOUND).build();
    }

    @PostMapping("/product/all")
    public ResponseEntity<List<ProductDTO>> getAllProducts(@RequestBody Map<String, String> map){
        List<ProductDTO> list = inventoryService.getAllProductStock();
        
        return (list != null && !list.isEmpty()) ? ResponseEntity.ok(list) : ResponseEntity.status(HttpStatus.NOT_FOUND).build();
    }
    
}
