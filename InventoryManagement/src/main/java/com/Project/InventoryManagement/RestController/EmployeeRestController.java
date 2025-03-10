package com.Project.InventoryManagement.RestController;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.Project.InventoryManagement.Service.InventoryService;

@RestController
@RequestMapping("/employee")
public class EmployeeRestController extends UserRestController{
    @Autowired
    public EmployeeRestController(InventoryService inventoryService){
        this.inventoryService = inventoryService;
    }
}
