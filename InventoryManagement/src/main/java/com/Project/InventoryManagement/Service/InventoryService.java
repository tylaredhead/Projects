package com.Project.InventoryManagement.Service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.Project.InventoryManagement.Entity.*;
import com.Project.InventoryManagement.Repository.*;


@Service
public class InventoryService {
    @Autowired
    private StockRepository stockRepo;
    @Autowired
    private SupplierRepository supplierRepo;
    @Autowired
    private ProductRepository productRepo;

    public Stock saveStock(Stock stock){
        return stockRepo.save(stock);
    }
   
    public List<Stock> getAllStock(){
        return stockRepo.findAll();
    }
   
    public List<Stock> findById(int id){
        return stockRepo.findById(id);
    }
   
    public List<Stock> findByRating(String rating){
        return stockRepo.findByRating(rating);
    }

    public List<Stock> findByQuantity(int quantity){
        return stockRepo.findById(quantity);
    }

    public Stock updateRating(int id, String rating){
        Stock stock = stockRepo.findById(id);
        stock.setRating(rating);
        return stockRepo.save(stock);
    }

    public Stock updateQuantity(int id, int quantity){
        Stock stock = stockRepo.findById(id);
        stock.setQuantity(stock.getQuantity() + quantity);
        return stockRepo.save(stock);
    }

    public void deleteById(int id){
        stockRepo.deleteById(id);
    }

    public Supplier saveSupplier(Supplier supplier){
        return supplierRepo.save(supplier);
    }

    public List<Supplier> getAllSuppliers(){
        return supplierRepo.findAll();
    }

    public List<Supplier> findBySupplierId(int id){
        return supplierRepo.findBySupplierId(int id);
    }

    public List<Supplier> findBySupplierName(String name){
        return supplierRepo.findBySupplierName();
    }

    public List<Supplier> findBySupplierNo(String no){
        return supplierRepo.findBySupplierNo(String no);
    }

    public List<Supplier> findBySupplierEmail(int email){
        return supplierRepo.findBySupplierEmail(String email);
    }

    public Supplier updateSupplierName(int id, String name){
        Supplier supplier= supplierRepo.findById(id);
        supplier.setSupplierName(name);
        return supplierRepo.save(supplier);
    }

    public Supplier updateSupplierName(int id, String no){
        Supplier supplier= supplierRepo.findById(id);
        supplier.setSupplierNo(no);
        return supplierRepo.save(supplier);
    }

    public Supplier updateSupplierEmail(int id, String email){
        Supplier supplier= supplierRepo.findById(id);
        supplier.setSupplierEmail(email);
        return supplierRepo.save(supplier);
    }

    public void deleteById(int id){
        supplierRepo.deleteById(id);
    }

    public void deleteBySupplierName(String name){
        supplierRepo.deleteBySupplierName(name);
    }

}