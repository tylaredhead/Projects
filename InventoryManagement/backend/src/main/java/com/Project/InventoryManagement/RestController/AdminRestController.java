package com.Project.InventoryManagement.RestController;


import java.util.List;
import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.Project.InventoryManagement.DTO.ProductDTO;
import com.Project.InventoryManagement.DTO.SuccessMsg;
import com.Project.InventoryManagement.Entity.Product;
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

    @PostMapping("/save/stock")
    public ResponseEntity<Stock> saveStock(@RequestBody Stock stock){
        stock = inventoryService.saveStock(stock);
        return ResponseEntity.ok(stock); 
    }

    @PostMapping("/save/supplier")
    public ResponseEntity<Supplier> saveSupplier(@RequestBody Supplier supplier){
        supplier = inventoryService.saveSupplier(supplier);
        return ResponseEntity.ok(supplier);
    }
    @DeleteMapping("/product/delete")
    public ResponseEntity<SuccessMsg> deleteBySupplierId(@RequestBody Map<String, String> map){
        String name = map.get("name");
        String type = map.get("type");
        int id;
        try {id = Integer.parseInt(map.get("id"));}
        catch (Exception e) { id = -1;}

        List<ProductDTO> productDTO;
        if (id != -1) {
            inventoryService.deleteByProductId(id);
            inventoryService.deleteById(id);
        } else if (name != "" && type != "") {
            productDTO = inventoryService.getProductsStockByNameAndType(name, type);
            for (ProductDTO p: productDTO){
                inventoryService.deleteByProductId(p.getId());
                inventoryService.deleteById(p.getId());
            }
        } else if (name != "") {
            productDTO = inventoryService.getProductsStockByName(name);
            for (ProductDTO p: productDTO){
                inventoryService.deleteByProductId(p.getId());
                inventoryService.deleteById(p.getId());
            }
        } else if (type != "") {
            productDTO = inventoryService.getProductsStockByType(type);
            for (ProductDTO p: productDTO){
                inventoryService.deleteByProductId(p.getId());
                inventoryService.deleteById(p.getId());
            }
        }
        
        return ResponseEntity.ok(new SuccessMsg());
    }

    @DeleteMapping("/supplier/delete")
    public ResponseEntity<SuccessMsg> deleteSupplier(@RequestBody Map<String, String> map){
        String name = map.get("name");
        int id;
        try {id = Integer.parseInt(map.get("id"));}
        catch (Exception e) { id = -1;}
        if (!name.equals("")) inventoryService.deleteBySupplierName(name);
        else if (id != -1) inventoryService.deleteBySupplierId(id);

        return ResponseEntity.ok(new SuccessMsg());
    }

    @PostMapping("save/product")
    public ResponseEntity<Product> saveProduct(@RequestBody Product product){
        product = inventoryService.saveProduct(product);
        return ResponseEntity.ok(product);
    }

    @PostMapping("supplier/update")
    public ResponseEntity<List<Supplier>> updateSupplier(@RequestBody Map<String, String> map){
        String name = map.get("name");
        String field = map.get("field");
        String value = map.get("value");

        int id;
        try { 
            id = Integer.parseInt(map.get("id"));
        } catch (Exception e) {
            id = -1;
        }
        
        List<Supplier> suppliers = inventoryService.getSuppliers(id, name);
        if (suppliers == null) return ResponseEntity.status(HttpStatus.NOT_FOUND).build();
        for (Supplier s: suppliers) {
            if (field.equals("Name")) {
                inventoryService.updateSupplierName(s.getSupplierId(), value);
            } else if (field.equals("Phone No")) {
                inventoryService.updateSupplierNo(s.getSupplierId(), value);
            } else if (field.equals("Email")) {
                inventoryService.updateSupplierEmail(s.getSupplierId(), value);
            } else return ResponseEntity.status(HttpStatus.NOT_FOUND).build();
        }
        return ResponseEntity.ok(suppliers);    
    }

    @PostMapping("/product/update")
    public ResponseEntity<SuccessMsg> updateProduct(@RequestBody Map<String, String> map){
        String name = map.get("name");
        String type = map.get("type");
        String field = map.get("field");//['Name', 'Type', 'Price', 'Quantity', 'Desc']
        String value = map.get("value");
        int id;
        try { 
            id = Integer.parseInt(map.get("id"));  
        } catch (Exception e) { id = -1; }

        List<ProductDTO> productDTO;
        if (id != -1) {
            productDTO = inventoryService.getProductStockById(id);
        } else if (name != "" && type != "") {
            productDTO = inventoryService.getProductsStockByNameAndType(name, type);
        } else if (name != "") {
            productDTO = inventoryService.getProductsStockByName(name);
        } else if (type != "") {
            productDTO = inventoryService.getProductsStockByType(type);
        } else return ResponseEntity.status(HttpStatus.BAD_REQUEST).build();
        for (ProductDTO p: productDTO) {
            System.out.println(field);
            if (field.equals("Name")) inventoryService.updateProductName(p.getId(), value);
            else if (field.equals("Type")) inventoryService.updateProductType(p.getId(), value);
            else if (field.equals("Price")) inventoryService.updatePrice(p.getId(), Float.parseFloat(value));
            else if (field.equals("Quantity")) inventoryService.updateQuantity(p.getId(), Integer.parseInt(value));
            else if (field.equals("Desc")) inventoryService.updateProductDesc(p.getId(), value);
        }

        return ResponseEntity.ok(new SuccessMsg());
    }
}
